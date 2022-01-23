
from test import Test

#Test.generateInstances()
#Test.PLS()
#Test.incrementalElicitation()
#Test.simulatedRandomIncrementalElicitation(mode="OWA")
#Test.simulatedRandomIncrementalElicitation(mode="WS")

#Test.PLSwithElicitation(mode="OWA")
#Test.PLSwithElicitation(mode="WS")

#Test.compare()

### Génère les logs de comparaison
#Test.generateLogs(10, mode="OWA")
#Test.generateLogs(5, mode="WS")

### Affiche les logs des deux procédures
#Test.loadLogs(mode="OWA")
Test.loadLogs(mode="WS")

###Generate logs de questions

#Obselete ne pas utiliser
#Test.generateQuestionsLogs(1, "OWA")

### Affiche les graphes de nombre de questions pour les valeurs PMR
#Test.loadQuestionsLogs(0, 9, "WS")