import cv2
import numpy as np
import matplotlib.pyplot as plt

"""Classe que fará o carregamento e a leitura da imagem"""
class FormDetector:
    def load_image(self, path_image):
        image = cv2.imread(path_image)
        if image is None:
            raise ValueError(f"imagem não encontrada:{path_image}")
        return image

    def convert_to_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def apply_blur(self, image):
        return cv2.GaussianBlur(image, (5, 5), 0)

    def edge_detection(self, image):
        return cv2.Canny(image, 50, 150)

    def find_lines(self, imagem_bordas):
        contornos, _ = cv2.findContours(
            imagem_bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        return contornos

    def classify_forms(self, contornos, imagem_original):
        """Classifica formas geometricas.
        Classificaremos em triangulos, quadrados, circulos e outros"""
        formas = {
            "triangulos":0,
            "quadrados":0,
            "circulos":0,
            "outros":0
        }

        for contorno in contornos:
            perimetro = cv2.arcLength(contorno, True)
            aproximacao = cv2.approxPolyDP(contorno, 0.04 * perimetro, True)


            #logica de classificação
            if len(aproximacao) == 3:
                formas["triangulos"] += 1
                cv2.drawContours(imagem_original,[contorno],
                                 0, (0, 255, 0), 2)

            elif len(aproximacao) == 4:
                formas["quadrados"] += 1
                cv2.drawContours(imagem_original, [contorno],
                                 0, (0, 255, 0), 2)

            elif len(aproximacao) > 4:
                area = cv2.contourArea(contorno)
                perimetro_quadrado = perimetro * perimetro
                circularity = 4 * np.pi * area / perimetro_quadrado

                if circularity > 0.8:
                    formas["circulos"] += 1
                    cv2.drawContours(imagem_original, [contorno],
                                     0, (0, 0, 255), 2)
                else:
                    formas["outros"] += 1
            return formas






