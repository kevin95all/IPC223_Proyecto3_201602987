import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree
from io import BytesIO
import re


class Gestor:

    def __init__(self):
        self.lista_perfiles = []
        self.perfil = []
        self.palabras_excluidas = []
        self.lista_palabras = []

    def recibir_configuraciones(self, xml):
        if xml:
            doc = ET.fromstring(xml)
            lista_perfiles = doc.find('perfiles')
            perfiles = lista_perfiles.findall('perfil')
            descartadas = doc.find('descartadas')
            excluidas = descartadas.findall('palabra')

            for perfil in perfiles:
                nombre = perfil.find('nombre')
                lista_palabras = perfil.find('palabrasClave')
                palabras = lista_palabras.findall('palabra')
                self.perfil.append(nombre.text)

                for palabra in palabras:
                    self.lista_palabras.append(palabra.text)

                self.perfil.append(self.lista_palabras)
                self.lista_perfiles.append(self.perfil)
                self.lista_palabras = []
                self.perfil = []

            for palabra in excluidas:
                self.lista_palabras.append(palabra.text)

            self.palabras_excluidas.append('Eliminar')
            self.palabras_excluidas.append(self.lista_palabras)
            self.lista_palabras = []

        return 'Configuraciones cargadas con exito'

    def recibir_mensajes(self, xml):
        if xml:
            doc = ET.fromstring(xml)
            mensaje = doc.find('mensaje')
            palabras = self.obtener_lista_de_palabras(mensaje.text)

            return self.obtener_porcentaje_de_generos(palabras)

    def obtener_lista_de_palabras(self, mensaje):
        mensaje = re.sub(r'\s+', ' ', mensaje)
        mensaje = re.sub(r'[^\w\s]', '', mensaje)
        mensaje = re.sub(r'\b\d+\b', '', mensaje)
        palabras = mensaje.lower().split()
        palabras = self.eliminar_palabras(palabras)

        return palabras

    def eliminar_palabras(self, palabras):
        excluidas = self.palabras_excluidas[1]
        for palabra in palabras:
            if palabra.lower() in [eliminar.lower() for eliminar in excluidas]:
                palabras.remove(palabra)

        return palabras

    def obtener_porcentaje_de_generos(self, palabras):
        total_palabras = len(palabras)
        root = Element('respuesta')
        SubElement(root, 'totalpalabras').text = str(total_palabras)
        categorias = SubElement(root, 'categorias')

        for genero, palabrasgenero in self.lista_perfiles:
            if genero != self.palabras_excluidas[0]:
                coincidencias = 0
                for palabra in palabras:
                    if palabra.lower() in [p.lower() for p in palabrasgenero]:
                        coincidencias += 1
                categoria = SubElement(categorias, 'categoria')
                SubElement(categoria, 'nombre').text = genero
                SubElement(categoria, 'coincidencias').text = str(coincidencias)
                SubElement(categoria, 'porcentaje').text = str((coincidencias / total_palabras) * 100)
        tree = ElementTree(root)
        xml_data = BytesIO()
        tree.write(xml_data, encoding='UTF-8', xml_declaration=True)
        return xml_data.getvalue()
