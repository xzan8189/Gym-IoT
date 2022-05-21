# IOT Gym using Serverless Computing

## Overview

Gym IoT is a gym that measures the calories consumed by the client, providing him with a constant report on the progress of his workout.
Inside the gyms there are machines that record informations about the calories consumed and the duration of the workout, but unfortunately these informations are ephemerals, they are not stored in any way (in a database) and for this reason there is no possibility to double-check these informations to understand how to improve your workout!

IoT Gym was created for this purpose, based on the informations collected from the training sessions, graphs are built, which can be viewed from the web-site, so as to keep track of the following informations:

* **Calories consumed** and **Time of use** on each machine in the gym
* **Total calories consumed each month** (you can compare the calories consumed in the current year with those in the previous year)
* **Calories consumed during the day**

The IoT sensors, positioned inside the machines, can  **measure incorrectly** the calories consumed and/or the time of use on the machine. If this occurs, a message is sent on the Error queue which triggers a Serverless Function which sends an email containing the <code>device ID</code>, which generated the error, the <code>value_time_spent</code> (usage time) and the <code>value_calories_spent</code> (calories consumed)


<div align="center">
<img src="./images/IFTTT.png" alt="loading..." width="80%" >
</div>

## Architecture


<div align="center">
<img src="./images/Architettura (image).png" alt="loading..." width="100%" >
</div>

* The IoT devices are simulated with a Python function using [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) 







* [english version](#sciot-project-idea)
* [italian version](#idea-progetto-sciot)


# SCIOT PROJECT IDEA

### DESCRIPTION:
Monitoring of the vital parameters of customers, who train inside the gym, thanks to IOT devices that are provided by the gym itself. Thanks to these devices, it accompanies the customer throughout his training cycle, providing him specific advantages:

### Proposed features

* **Obtaining a new training schedule**:
	* Control of the kilocalories consumed by the customer in order to reach, and perhaps exceed, the <code>ideal threshold</code> (calculated based on customer weight and height).\
	There will be a **loading bar**:
		* Once the loading bar it is <code>100%</code> filled then:
			1. it means that it is ready to receive a new advanced training card (or can keep the old one)
			<br></br>
		* if the loading bar stalls (or even has a significant dip), then:
			1. provide a less difficult training schedule,
			2. provide a graph that makes the customer aware of his performance on each individual machine, so as to understand on which machine he has been most "weak" (this feature is available both daily and monthly):
				* <code>usage time</code> of each machine,
				* <code>kilocalories consumed</code> on each machine,
				<br></br>
                
* **Constant monitoring of the use of the customer's machines**
	* If the customer is not performing the correct sequence of machines to be used, established within the training schedule, then he is notified. This is in order to get the best results from his training schedule.
	* If the customer exceeds his daily use time of a specific machine then he is immediately notified and reminded of the next machine to use (according to his training schedule)
	* Once the customer has exceeded his <code>total daily usage time</code> of the machines, his is notified by providing him with some information:
		* Graph of the <code>heart rate trend</code> of the training day
		* He is advised not to continue and therefore his training day should end.
<br></br>
<br></br>

# IDEA PROGETTO SCIOT

### DESCRIZIONE:
Controllo dei parametri vitali dei clienti, che si allenano all'interno della palestra, grazie a dei dispositivi IOT che vengono forniti dalla palestra stessa. Grazie a questi dispositivi si accompagna il cliente durante tutto il suo ciclo d’allenamento, fornendogli specifici vantaggi:

### Funzionalità proposte

*  **Ottenimento di una nuova scheda di allenamento**:
	* Controllo delle kilocalorie consumate da parte del cliente al fine di raggiungere, e magari superare, la <code>soglia ideale</code> (calcolata in base al peso e all’altezza del cliente).\
	Ci sarà una **barra di carimento**:
		* Una volta che la barra di caricamento è riempita al <code>100%</code>, allora:
			1. significa che è pronto a ricevere una nuova scheda di allenamento più avanzata (oppure può continuare, e quindi mantenere, quella che già ha).
			<br></br>
		* Se la barra di caricamento sta in una fase di stallo (o addirittura ha avuto un calo), allora:
			1. fornire una scheda di allenamento meno difficile (solo alla fine del mese),
			2. fornire un grafico che faccia rendere consapevole al cliente del suo andamento su ogni singola macchina, così da comprendere su quale macchina è stato più “fiacco” (questa funzionalità è disponibile sia giornalmente che mensilmente):
				*  <code>tempo di utilizzo</code> di ogni macchina,
				*  <code>kilocalorie consumate</code> su ogni macchina,
				<br></br>
 
*  **Monitoraggio costante dell’utilizzo delle macchine del cliente**
	* Se il cliente non sta eseguendo la corretta sequenza di macchine da utilizzare, stabilita all’interno della scheda di allenamento, allora gli viene notificato. Questo al fine di ottenere i migliori risultati dalla propria scheda d’allenamento.
	* Se il cliente supera il proprio tempo di utilizzo giornaliero di una specifica macchina allora viene immediatamente notificato e gli viene ricordato la prossima macchina da utilizzare (secondo la scheda d’allenamento)
	* Una volta che il cliente ha superato il proprio <code>tempo di utilizzo complessivo giornaliero</code> delle macchine viene notificato fornendogli alcune informazioni:
		* Grafico dell'<code>andamento del battito cardiaco</code>  della giornata d’allenamento
		* Gli viene consigliato di non continuare e che quindi la sua giornata di allenamento dovrebbe terminare.