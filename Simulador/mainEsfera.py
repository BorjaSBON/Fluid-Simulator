from visual import *
from particula import *
from sistemaParticulas import *
from fuente import *
from metodoIntegracion import *
from gestorColisiones import *
from vecinas import *
from dinamicas import *
from vecinosHash import *
import exportador

#Contenedor y Limites

caja = box(pos = vector(0.0,1.0,0.0), size = vector(3.0,5.0,3.0))
caja.opacity = 0.1

limiteX_inf = caja.pos.x - (caja.size.x / 2)
limiteX_sup = caja.pos.x + (caja.size.x / 2)

limiteY_inf = caja.pos.y - (caja.size.y / 2)
limiteY_sup = caja.pos.y + (caja.size.y / 2)

limiteZ_inf = caja.pos.z - (caja.size.z / 2)
limiteZ_sup = caja.pos.z + (caja.size.z / 2)

LimitesX = [limiteX_inf, limiteX_sup]
LimitesY = [limiteY_inf, limiteY_sup]
LimitesZ = [limiteZ_inf, limiteZ_sup]

LimitesCaja = (limiteX_inf, limiteX_sup, limiteY_inf, limiteY_sup, limiteZ_inf, limiteZ_sup)

# Objetos Entorno

esfera = sphere(pos = vector(0.0,-1.5,0), radius = 0.4)
esfera.opacity = 1.0

cilindro = cylinder(pos = vector(-1.0,-1.5,0.0), axis = vector(0.0,1.0,0.0), radius = 0.3)
cilindro.opacity = 1.0

cubo = box(pos = vector(1.0,-1.0,0.0), size = vector(0.5,1.0,0.5))
cubo.opacitu = 1.0

limiteCuboX_inf = cubo.pos.x - (cubo.size.x / 2)
limiteCuboX_sup = cubo.pos.x + (cubo.size.x / 2)

limiteCuboY_inf = cubo.pos.y - (cubo.size.y / 2)
limiteCuboY_sup = cubo.pos.y + (cubo.size.y / 2)

limiteCuboZ_inf = cubo.pos.z - (cubo.size.z / 2)
limiteCuboZ_sup = cubo.pos.z + (cubo.size.z / 2)

LimitesCubo = (limiteCuboX_inf, limiteCuboX_sup, limiteCuboY_inf, limiteCuboY_sup, limiteCuboZ_inf, limiteCuboZ_sup)

# Variables

cont = 0
deltat = 0.001
gravedad = vector(0.0,-9.81,0.0)

k = 1300.0
h = 0.18

# Variables Particulas y Fuente

posicionInicial = vector(0.0, 0.0 ,2.0)
velocidadInicial = vector(0.0, -1.0, 0.0)

radio = 0.04
separacion = 2.25 * radio

espesor = radio

# Variables SPH

alpha = 1.08 * h * h
beta = 1.768 * h
gamma = 31.16

mu = 0.66

# Exportador

nFrame = 0

# Generador de particulas

intervalo = int(radio * 1000)
vecesGenera = 75
tiempoTotalIntervalo = intervalo * vecesGenera
momento = pi / 10

sistemaGenerado = SistemaParticulas()
sistemaGenerado = generaColumnaEsfera(posicionInicial, 0.1, 15, separacion, velocidadInicial, radio)
cantidadParticulas = sistemaGenerado.getNumeroParticulas()
print(cantidadParticulas)

# Bucle de Simulacion

while cont < 7500:
    #rate(100)
    print("Paso " + str(cont))
    print("------------")

    # Calculamos Vecinas y Fuerzas Internas
    
    sistema = sistemaGenerado.sistemaParticulas
    calculaVecinosHash(sistema, h)
    
    vecindad = Dinamicas()
    vecindad.LeyDeHook(sistemaGenerado, k, h)

    vecindad.calculoDensidades(sistema, alpha, h)
    vecindad.SPH(sistema, alpha, beta, gamma, k, mu, h)
    
    for i in range(cantidadParticulas):
        particula = sistemaGenerado.getParticula(i)

        # Calculamos si hay Colisiones

        gestorMult = gestorColisionesLimites(LimitesCaja, LimitesCubo, esfera.pos, esfera.radius, cilindro.pos, cilindro.radius, cilindro.axis, espesor, particula)
        
        if gestorMult[0] == False and gestorMult[1] == False and gestorMult[2] == False and gestorMult[3] == False:
            fuerzaInterna = particula.getFuerzaInterna()
            fuerzaPresion = particula.getFuerzaPresion()
            fuerzaViscosidad = particula.getFuerzaViscosidad()
            fuerzaTotal = fuerzaInterna + fuerzaPresion + fuerzaViscosidad
            particula.setFuerzaTotal(fuerzaTotal)
            
        elif gestorMult[0] == True or gestorMult[1] == True or gestorMult[2] == True or gestorMult[3] == True:
            gestorMult[0] == False
            gestorMult[1] == False
            gestorMult[2] == False
            gestorMult[3] == False
            particula.setFuerzaTotal(vector(0.0, 0.0, 0.0))
        
        # Calculamos la nueva Posicion y Velocidad de la Particula
        
        metodo = MetodoEuler(particula, gravedad, deltat)
        particula.setPosicion(metodo[0])
        particula.setVelocidad(metodo[1])
    
    if cont%15 == 0:
        exportador.exportar("pruebaEsf", nFrame, sistema, radio)
        nFrame += 1
    
    cont += 1
