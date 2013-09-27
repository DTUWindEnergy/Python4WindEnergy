from latex_generator.slides import *

### Don't forget to use 2 \\ if you want to have 1 \ in your .tex file!

s = slides(
  tex_filename= '20130925_WindPowerMonthlysForum_Rethore.tex',
  short_title = 'Uncertainty \& Wake',
  title = """Evaluation of the Wind Direction Uncertainty And Its Impact on Wake Modelling at the Horns Rev Offshore Wind Farm""",
  date = 'Windpower Monthly\'s Wind Farm Data \\\\ Management and Analysis forum \\\\ 23-25 September',
  author= "Pierre-Elouan R\\'{e}thor\\'{e}*, Mathieu Gaumond, Andreas Bechmann, Kurt Hansen, Alfredo Pena, S\\o{}ren Ott, Gunner Larsen",
  short_author = "P.-E. R\\'{e}thor\\'{e}",
  institute = "Aero-elastic Section, Wind Energy Department, DTU, Ris\\o{}"
)

### Create the outline of the presentation using the sections and subsections
s.f('Outline','\\tableofcontents')

s.section('Why Uncertainty Matters?', 'Uncertainty')
s.subsection('Introduction')
s.f('Overview of DTU\'s Wind Farm Flow Models',
  cfig('figs/screenshot.png'))

s.f('What Are Those Models used for?', columns([itemize([
    'Estimating Annual Energy Production',
    'Wind Farm Optimization']),
    fig('figs/screenshot.png')]))

s.f('The Horns Rev test case - Western winds',
  centered(fig('figs/horns_rev_test_case.png',width='0.8\\textwidth')))

s.f('Results of the Wake Model Benchmarking: \\\\ Confusion!',
  columns([[centered(['$270^\circ \pm 2.5^\circ$', fig('figs/wf_25', width='0.25\\textwidth')]), cfig('figs/hr_25')],
           [centered(['$270^\circ \pm 15^\circ$', fig('figs/wf_15', width='0.25\\textwidth')]), cfig('figs/hr_15')],]))

for i in range(4):
    s.f('The effect of wind direction uncertainty on wind farm wake measurement', 
      cfig('figs/anim%d'%(i+1), width='0.9\\textwidth'))

s.f('Sources of wind direction uncertainty',
  [block(itemize([
    'Yaw misalignment (when yaw sensor is used to measure direction)',
    'Time drift of the calibration',
    'Failures']),
    title='Random/temporal bias from the measurement device', order='1-'),
   block(itemize([
    'Small scale turbulence (sub 10-minute) \\\\ -> This {\it should} be accounted by the models',
    'Large scale turbulence (i.e. wind directional trends, over 10-minute)'
    ]), title='Atmospheric turbulence', order='2-'),   
   block(itemize([
    'Spatial variability of the wind direction',
    'Different time-control volume averaging'
   ]), title='Wind direction coherence', order='3-')])
 
s.f('Spatial decorrelation of wind direction',[
  block("""The wind direction correlation between M2 and the wind turbines decreases linearly with 
        the distance"""),
  columns([cfig('figs/Horns_rev_M2'), cfig('figs/std_increase')])])

s.f('Outline','\\tableofcontents')
s.subsection('Method: {\small Modelling the wind direction uncertainty}')

s.f('The "traditional" method', columns([itemize([
        'Step 1: Run simulations with fixed and homogeneous wind direction covering the desired wind direction sector',
        'Step 2: Apply a linear average to reproduce the data post-processing']),
           cfig('figs/traditional_method', width='0.74\\textwidth')], position='t'))


s.f('The proposed method', columns([itemize([
        'Step 1: Run simulations with fixed and homogeneous wind direction']),
         cfig('figs/method0')], position='t'))
s.f('The proposed method', columns([itemize([
        'Step 1: Run simulations with fixed and homogeneous wind direction',
        'Step 2: Apply a weighted average based on the probability function of a normal distribution on the interval $\pm 3 \sigma$']),
         cfig('figs/method1')], position='t'))
s.f('The proposed method', columns([itemize([
        'Step 1: Run simulations with fixed and homogeneous wind direction',
        'Step 2: Apply a weighted average based on the probability function of a normal distribution on the interval $\pm 3 \sigma$']),
         cfig('figs/method2')], position='t'))
s.f('The proposed method', columns([itemize([
        'Step 1: Run simulations with fixed and homogeneous wind direction',
        'Step 2: Apply a weighted average based on the probability function of a normal distribution on the interval $\pm 3 \sigma$',
        'Step 3: Apply a linear average to reproduce the data post-processing']),
         cfig('figs/method3')], position='t'))

s.subsection('Results')
s.f('All the rows, using a row-specific wind direction uncertainty', [
  columns([[centered(['$270^\circ \pm 2.5^\circ$', fig('figs/wf_25', width='0.25\\textwidth')])],
           [centered(['$270^\circ \pm 15^\circ$', fig('figs/wf_15', width='0.25\\textwidth')])]]),
  cfig('figs/wf_125_corrected')])

for i in range(3):
  s.f('Result for the whole wind farm in $\\theta = 270^\circ$',
    cfig('figs/result_table%d'%(i)))

s.section('Adding Value to Wind Farm Data', 'Wind Farm Data')
s.f('Outline','\\tableofcontents')
s.subsection('Machine Learning and Physical Modelling')

for i in range(2): 
  s.f('From Deterministic to Stochastic',cfig('figs/desto%d'%(i)))

for i in range(3): 
  s.f('System Engineering',cfig('figs/system%d'%(i)))

s.subsection('The FUSED-Wind project')
s.f('Connecting All Wind Energy Models in a Worflow', columns([itemize([
  'Collaborative effort between DTU and NREL to create a {\\bf F}ramework for {\\bf U}nified {\\bf S}ystem {\\bf E}ngineering and {\\bf D}esigned of {\\bf Wind} energy plants.',
  'Based on OpenMDAO, a python based Open source framework for {\\bf M}ulti-{\\bf D}isciplinary {\\bf A}nalysis and {\\bf O}ptimization.',
  'FUSED-Wind will offer built in capabilities for Uncertainty Quantification, Machine Learning and Optimization']),
  cfig('figs/FUSED_wind')]))

s.subsection('A Future Business Concept')

for i in range(7):
  s.f('', cfig('figs/concept%d'%(i)))

s.section('Conclusion and Future Works')
s.f('Conclusion', itemize([
    'The N.O. Jensen model, the G.C. Larsen model and Fuga are robust engineering models able to provide accurate predictions using wind direction sectors of $30^\circ$',
    'The discrepancies for narrow wind direction sectors are not caused by a fundamental inaccuracy of the current wake models, but rather by a large wind direction uncertainty included in the dataset',
    'We need some models and measurements for wind direction uncertainty to move forwards from this stage',
    '\color{red}{Do not "tune" your wake models to match the $\pm2.5^\circ$ measurements!!!}']))
           
s.f('Future work',[block(itemize([
    'The method will be applied to other wake models and datasets',
    'Sample based uncertainty quantification to be investigated',
    'Work on estimating the wind direction uncertainty using the wind farm dataset']),
     title='Wind Farm Flow Model Uncertainty'),
    block(itemize([
    'Opening FUSED-Wind to the public',
    'Adding Uncertainty Quantification to FUSED-Wind',
      ]), title='System Engineering')])

s.f('Thank you for your attention!',
  [itemize(['Work funded by EUDP-WakeBench and EERA-DTOC',
            'Dataset graciously made available by DONG Energy and Vattenfall.',
            'Article submitted to wind energy and master thesis available on request']),
  cfig('figs/publications')])


#s.frame(doc_main = [
#    block('This is block 1', title = 'Block 1'),
#    columns([column(block('This is block 2')),
#             column(block('This is block 3'))])], title = 'new frame')


#f1.add('This is a normal text')

s.compile()