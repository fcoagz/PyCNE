import requests
import json

base_url = 'http://www.cne.gob.ve/web/registro_electoral/ce.php'

class consulta():
    def __init__(self, nacionalidad, cedula, altmode=False, base_url=base_url):
        self.nacionalidad = nacionalidad
        self.cedula = cedula
        self.base_url = base_url

        try:
            self.response = requests.get(f'{self.base_url}?nacionalidad={self.nacionalidad}&cedula={self.cedula}')
        except:
            raise ConnectionError(self.err(1))
        
        if not altmode:
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(self.response.content, 'html.parser') 
            data = []
            
            for i in soup.find_all('td', {'align': 'left'}):
                if i.find('font',color='#00387b'):
                    pass
                else:
                    data.append(i.text)
                        
            if data ==  []:
                raise Exception(self.err(0))
            
            self.cedula = data[0]
            self.nombre = data[1]
            self.estado = data[2]
            self.municipio = data[3]
            self.parroquia = data[4]
            self.centro = data[5]
            self.direccion = data[6]

        else:
            import re
            cleanhtml = re.sub('<.*?>', '', self.response.text)
            cleancomments = re.sub('-->','', cleanhtml)
            cleantext = " ".join(cleancomments.split())
                
            if re.findall(r'Esta cédula de identidad no se encuentra inscrito en el Registro Electoral.', cleantext):
                raise Exception(self.err(0))
                
            cedula = re.findall(r'Cédula:\s[a-zA-Z]-[0-9]+', cleantext)
            nombre = re.search(r'Nombre:\s([a-zA-Z]+( [a-zA-Z]+)+)\s', cleantext).group(0)
            estado = re.findall(r'Estado:\s[a-zA-Z.]+\s*[a-zA-Z]*', cleantext)
            municipio = re.search(r'Municipio:\s([a-zA-Z. ]*[a-zA-Z.])+\s', cleantext).group(0)
            parroquia = re.search(r'Parroquia:\s([a-zA-Z. ]*[a-zA-Z.])+\s', cleantext).group(0)
            centro = re.search(r'Centro:\s([a-zA-Z. ]*[a-zA-Z.])+\s', cleantext).group(0)
            direccion = re.search(r'Dirección:\s([a-zA-Z. ]*[a-zA-Z.])+\s', cleantext).group(0)
                
            cedula = cedula[0].split(': ')
            nombre = nombre.split(': ')
            estado = estado[0].split(': ')
            municipio = municipio.split(': ')
            parroquia = parroquia.split(': ')
            centro = centro.split(': ')
            direccion = direccion.split(': ')
                
            self.cedula = cedula[1]
            self.nombre = nombre[1].rstrip()
            self.estado = estado[1]
            self.municipio = municipio[1].rstrip()
            self.parroquia = parroquia[1].rstrip()
            self.centro = centro[1].rstrip()
            self.direccion = direccion[1].rstrip()
            
        self.info = {'cedula':self.cedula,
                    'nombre':self.nombre,
                    'estado':self.estado,
                    'municipio':self.municipio,
                    'parroquia':self.parroquia,
                    'centro':self.centro,
                    'direccion':self.direccion}

        self.info_json = json.dumps(self.info)      
                

    class multi(): 
        def __init__(self, data, altmode=False, base_url=base_url):
            
            self.info = []
            self.errors = []
            
            for i in data:
                try:
                    i = i.split('-')
                    i_consulta = consulta(i[0],i[1],altmode=altmode,base_url=base_url)
                    self.info.append(i_consulta.info)
                except ConnectionError:
                    raise
                except:
                    self.errors.append('-'.join(i))
            
            if data == []:
                raise Exception(consulta.err(self, 2))
            
            self.errors_json = json.dumps(self.errors)
            self.info_json = json.dumps(self.info)

    def err(self, error_code):
        
        if type(self).__name__ == 'multi':
            self.nacionalidad = ''
            self.cedula = ''
            
        err = {
            '0':f'[PyCNE] La cédula {self.nacionalidad}-{self.cedula} no se encuentra inscrita en el CNE.',
            '1':f'[PyCNE] No se ha podido establecer la conexión con el servidor.',
            '2':f'[PyCNE] Los parámetros de la consulta están vacíos.'
        } 

        return err[f'{error_code}']