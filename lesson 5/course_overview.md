## Outline
\tableofcontents

# OpenMDAO concepts

## OpenMDAO concepts
\centering{\includegraphics[width=0.7\textwidth]{imgs/component-driver-workflow-asmb-1024x867.png}}

## In practice
\centering{\includegraphics[width=0.9\textwidth]{imgs/concept.png}}

## Example: The Rozenbrock optimization
The Rozenbrock function: $f=100 (x2 - x1^2)^2 + (1 - x1)^2$

\centering{\includegraphics[width=0.6\textwidth]{imgs/rozenbrock.png}}

## Component definition
```python
class Rosenbrock(Component):
    """ Standard two-dimensional Rosenbrock function. """

    x1 = Float(iotype='in')
    x2 = Float(iotype='in')
    f  = Float(iotype='out')

    def execute(self):
        """ Just evaluate the function. """
        x1 = self.x1
        x2 = self.x2
        self.f = 100 * (x2 - x1**2)**2 + (1 - x1)**2
```

## Assembly definition
```python
class Optimization(Assembly):
    def configure(self):
        """ Configure driver and its workflow. """
        super(Assembly, self).configure()
        self.add('rosenbrock', Rosenbrock())
        self.add('driver', CONMINdriver())
        self.driver.workflow.add('rosenbrock')
        self.driver.add_parameter('rosenbrock.x1', 
                            low=-2, high=2, start=-1.0)
        self.driver.add_parameter('rosenbrock.x2', 
                            low=-2, high=2, start=-2.0)
        self.driver.add_objective('rosenbrock.f')

        # Some additional optimizer options
        #...

opti = Optimization()
opti.run()
```

## Rosenbrock optimization
After a few iterations...

\centering{\includegraphics[width=0.8\textwidth]{imgs/rosenbrock_optimization.pdf}}

## Different types of Drivers:
* Optimizers (support for gradients)
    * Natives (COBYLA, CONMIN, Genetic, NEWSUMT, SLSQP)
    * DAKOTA plugin (20+)
    * pyOpt plugin (10+)
    * more..
* CaseIteratorDriver: loop through a list of cases, possibly in parallel
* Design of Experiment: do parameter studies
* Sampling...

## Different types of variables

* Array 
* Bool  
* Complex
* Enum  
* File  
* Float 
* Int   
* Slot  
* Str   

## Different types of Assembly usage (1/2)
Several nested drivers within one assembly


\centering{\includegraphics[width=0.8\textwidth]{imgs/IterationHierarchy.png}}

## Different types of Assembly usage (1/2)
Nested assemblies


\centering{\includegraphics[width=0.8\textwidth]{imgs/Intro-Driver1.png}}

## GUI
There is web-based GUI, that you can use to explore your assemblies:

\centering{\includegraphics[width=0.8\textwidth]{imgs/GUI.png}}

[youtube](http://www.youtube.com/watch?v=BK73Zria9OI)

# Work on OpenMDAO at DTU

## Projects (1/3)
### Topfarm (Pierre-Elouan)
Wind Farm Layout optimization

* Wake models (FUSED-Wake)
* Foundation cost
* Electrical grid cabling cost model
* Wind Farm Financial Balance
* \gray{DWM HAWC2 Fatigue database}
* \gray{WAsP-CFD}

. . .

### FUSED-Wake (Pierre-Elouan)
Framework for analysis of wind farm wake models:
`NOJensen`, `GCL`, `Ainslie`, `FUGA`, \gray{DWM}, \gray{EllipSys3D AD/AL}

* Uncertainty Quantification
* Model Averaging
* Multi-fidelity modelling



## Projects (2/3)
### Light Rotor
* Wind turbine optimization 
    * aerodynamic (`HAWC2` & `HAWCStab2`) (Frederik, Carlo)
    * structural (`Becas`, `CSProps`) (David, Witold)
* Airfoil optimization
    * Aerodynamic (`XFoil`, `EllipSys2D`) (Frederik, Franck)
    * Noise model (`TNO`, `XFoil`) (Franck)

. . .

### Aero-servo-elastic optimization (Carlo's PhD)
`HAWCStab2` & `HAWC2`


## Projects (3/3)

### `Ellipsys`-`HAWC2` coupling
* Coupling between `EllipSys3D` fully resolved and `HAWC2` (Joachim)
* Coupling between `EllipSys3D` Actuator Disc/Line and `HAWC2`(aero) (Niels T)

### Topology optimization (Alexander)

## Wrapped Codes
* Operational
    * EllipSys3D
    * Becas
    * HAWC2
    * HAWCStab2
    * XFoil
    * CSProps
* Under development / Planned
    * \gray{FUGA}
    * \gray{DWM-HAWC2}
    * \gray{WAsP}
    * \gray{WAsP-CFD}
    * \gray{WRF}
    * \gray{CORWIND}

# Work on OpenMDAO at NREL


# FUSED-Wind 
# OpenMDAO guided tutorial
# OpenMDAO exercise
