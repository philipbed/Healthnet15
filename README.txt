#Root User - Super user#
Username: admin Password: admin

#Hospital Admins#
Username: admindexter   Password: password
Username: adminkrutz    Password: password
Username: rockstar      Password: password
Username: coolville     Password: susancool

#Doctors#
Username: doctorswag    Password: password
Username: doctorjohn    Password: password
Username: doctorstorm   Password: password
Username: doctorsusan   Password: password

#Nurses#
Username: nursejackie   Password: password
Username: nursejess     Password: password
Username: nursedamme    Password: password
Username: efron         Password: password

#Patients#
Username: dxh9845       Password: gucun43
Username: bswag         Password: password
Username: gh1823        Password: password
Username: philly        Password: 123456
Username: johnboard     Password: superc00l

#Preface

This is guide to set this python and django based project up and running.
The versions that are required to run this are Python 3.4.3, Django 1.8.3, Sqlite 3.7.11.

# Introduction

This is healthnet, an online resource that will help hospitals be more efficient. 


#Install

This install process will assume that the user already has python and django installed. 


	<set up>
	1. Unzip folder to desired destination.
	2. Open a command line to unzip location.
	3. type "cd healthnet".
	4. type "python manage.py runserver".

	This will run the server at default setting which will be fine.

	<using site>
	1. Open your web browser and type "localhost:8000"

	This is the landing page for Healthnet, there are multiple options but first lets get you registered.

<Patient functions>

	<registration>
	1. Hit "Register".
	2. Fill out all fields.
	3. Hit "Register".
		Warning: if fields aren't correct page will give you errors until fixed.

	You are now registered with Healthnet congratulations.

	<Login>
	1. Type "localhost:8000/healthnet/home"
	2. Hit "Login"
	3. Enter credentials
	4. hit "login" 

	<view/change profile>
	1. Hit "Profile".
	2. If entered correctly you will now see your current information.
	3. To change this hit "Edit profile".
	4. Enter new information and hit "Update".

	Lets make an appointment

	<making an appointment>
	1. Hit "Return to profile".
	2. Hit "appointments".
	3. Hit "schedule".
	4. Fill out fields.
	
	<changing an appointment>
	1. Hit "Appointment List".
	2. Hit "edit" on the appointment you want to change. 
	3. Make the changes and hit "Save"

	Now that we have all these appointments lets view them all!
	
	<Calender>	
	1. Hit "Appointment list"
	2. Hit "schedule"

	<Delete appointment>
	1. hit "appointments".
	2. hit delete on the preferred appointment.
	3. hit "submit".

	<log out>
	1. Hit "appointment list"
	2. Hit "Profile"
	3. Hit "Logout"

	<View prescription>
	1. Hit �Prescription� at the top of the page
	2. Now you should be seeing all prescriptions that have beeen prescribed to you.
	
	<View Inbox>
	1. Hit �View your Messages� under Messaging at the to of the page.
	2. Now you should be seeing your entire in box.

	<View Sent messages>
	1. Hit �View your sent Messages� under Messaging at the to of the page.
	2. Now you should be seeing your sent box.

	<Sending a Message>
	1. Hit �Send a Message� under Messaging at the to of the page.
	2. choose the recipaint from the drop down and the top left.
	3. Then fill in the subject just under the drop down.
	4. Next fill in your message under the Body field.
	5. Lastly hit send, you should be prompted with a confirmation saying that the message was sent.

	<Replying to a Message>
	1. Hit �View your Messages� under Messaging at the to of the page.
	2. Now you should be seeing your entire in box.
	3. Click reply under one of the received messages
	4. Next fill in the body under the subject line.
	5. Lastly hit send at the bottom right of the page.

	<add preferred hospital>
	1. Click on your name at the top of the landing page.
	2. Now click on the �View Profile� in the drop down.
	3. Now click �add your preferred hospitals�
	4. Select a hospital from the drop down.
	5. Lastly hit add hospital
 
	<add medical history>
	1. Click on your name at the top of the landing page.
	2. Now click on the �View Profile� in the drop down.
	3. Now click �add medical history�
	4. Fill out the form
	5. hit submit at the bottom right

	<update medical history>
	1. Click on your name at the top of the landing page.
	2. Now click on the �View Medical history� in the drop down.
	3. Now click �update� in the top center of the screen.
	4. Fill out the form.
	5. Hit submit at the bottom right.


	<Logging out>
	1. Click on your name at the top of the landing page.
	2. Now click on the �Logout� in the drop down.

<Nurse functions>

	<View Inbox>
	1. Hit �View your Messages� under Messaging at the to of the page.
	2. Now you should be seeing your entire in box.

	<View Sent messages>
	1. Hit �View your sent Messages� under Messaging at the to of the page.
	2. Now you should be seeing your sent box.

	<Sending a Message>
	1. Hit �Send a Message� under Messaging at the to of the page.
	2. choose the recipaint from the drop down and the top left.
	3. Then fill in the subject just under the drop down.
	4. Next fill in your message under the Body field.
	5. Lastly hit send, you should be prompted with a confirmation saying that the message was sent.

	<Replying to a Message>
	1. Hit �View your Messages� under Messaging at the to of the page.
	2. Now you should be seeing your entire in box.
	3. Click reply under one of the received messages
	4. Next fill in the body under the subject line.
	5. Lastly hit send at the bottom right of the page.

	<getting to the dango admin panel>
	1. Log in as root
	2. click Admin Interface at the top of the page.

	<view Patients>
	1. hit Patients, then hit view Patients

	<view specific patient>
	1. hit Patients, then hit view Patients
	2. Hit View Details

	<transfer patient>
	1. hit Hospitals, then hit view Patients
	2. Hit View Details
	3. Hit Transfer at the bottom left of the page

	<View medical history>
	Note: this is only if there is medical history for that patient
	1. hit Hospitals, then hit view Patients
	2. Hit View Details
	3. Hit View at the bottom right of the page

	<making an appointment>
	1. Hit "Return to profile".
	2. Hit "appointments".
	3. Hit "schedule".
	4. Fill out fields.
	
	<changing an appointment>
	1. Hit "Appointment List".
	2. Hit "edit" on the appointment you want to change. 
	3. Make the changes and hit "Save"

	Now that we have all these appointments lets view them all!
	
	<Calender>	
	1. Hit "Appointment list"
	2. Hit "schedule"

<Doctor function>

	<View Inbox>
	1. Hit �View your Messages� under Messaging at the to of the page.
	2. Now you should be seeing your entire in box.

	<View Sent messages>
	1. Hit �View your sent Messages� under Messaging at the to of the page.
	2. Now you should be seeing your sent box.

	<Sending a Message>
	1. Hit �Send a Message� under Messaging at the to of the page.
	2. choose the recipaint from the drop down and the top left.
	3. Then fill in the subject just under the drop down.
	4. Next fill in your message under the Body field.
	5. Lastly hit send, you should be prompted with a confirmation saying that the message was sent.

	<Replying to a Message>
	1. Hit �View your Messages� under Messaging at the to of the page.
	2. Now you should be seeing your entire in box.
	3. Click reply under one of the received messages
	4. Next fill in the body under the subject line.
	5. Lastly hit send at the bottom right of the page.
	
	<view Patients>
	1. hit Patients, then hit view Patients

	<view specific patient>
	1. hit Patients, then hit view Patients
	2. Hit View Details

	<transfer patient>
	1. hit Hospitals, then hit view Patients
	2. Hit View Details
	3. Hit Transfer at the bottom left of the page

	<View medical history>
	Note: this is only if there is medical history for that patient
	1. hit Hospitals, then hit view Patients
	2. Hit View Details
	3. Hit View at the bottom right of the page

	<give a patient a prescription>
	1. hit Hospitals, then hit view Patients
	2. Hit View Details
	3. hit add a proscription on the bottom left of the page
	4. Fill out the form
	5. click send
	
	<making an appointment>
	1. Hit "Return to profile".
	2. Hit "appointments".
	3. Hit "schedule".
	4. Fill out fields.
	
	<changing an appointment>
	1. Hit "Appointment List".
	2. Hit "edit" on the appointment you want to change. 
	3. Make the changes and hit "Save"

	Now that we have all these appointments lets view them all!
	
	<Calender>	
	1. Hit "Appointment list"
	2. Hit "schedule"

	<Delete appointment>
	1. hit "appointments".
	2. hit delete on the preferred appointment.
	3. hit "submit".

<Admin Function>

	<View Inbox>
	1. Hit �View your Messages� under Messaging at the to of the page.
	2. Now you should be seeing your entire in box.

	<View Sent messages>
	1. Hit �View your sent Messages� under Messaging at the to of the page.
	2. Now you should be seeing your sent box.

	<Sending a Message>
	1. Hit �Send a Message� under Messaging at the to of the page.
	2. choose the recipaint from the drop down and the top left.
	3. Then fill in the subject just under the drop down.
	4. Next fill in your message under the Body field.
	5. Lastly hit send, you should be prompted with a confirmation saying that the message was sent.

	<Replying to a Message>
	1. Hit �View your Messages� under Messaging at the to of the page.
	2. Now you should be seeing your entire in box.
	3. Click reply under one of the received messages
	4. Next fill in the body under the subject line.
	5. Lastly hit send at the bottom right of the page.

	<getting to the dango admin panel>
	1. Log in as root
	2. click Admin Interface at the top of the page.


	<filter Log> 
	1. Hit "system"
	2. Then under the system drop down hit Log
	3. You should now be seeing the log of the entire system.
	4. In the upper left there is a blue word filter, hit that 
	5. enter the dates and hit filter
	6. You should now see the filtered log

	<View Stats>
	1. Hit "system"
	2. Then under the system drop down hit statistics
	3. You should now be seeing the log of the entire system.

	<Filter Stats>
	1. Hit "system"
	2. Then under the system drop down hit statistics
	3. You should now be seeing the stats of the entire system.
	4. In the upper left there is a blue word filter, hit that 
	5. Enter the dates and select a hospital.
	6. Hit filter and you should now see the filtered statistics


	<create doctor>
	1. hit Hospitals, then hit create Doctor
	2. Fill out fields 
	3. click register

	<create Nurse>
	1. hit Hospitals, then hit create Nurse
	2. Fill out fields 
	3. click register

	<update doctor>
	1. hit Hospitals, then hit view personnel
	2. under the doctors subsection click on the desired doctor's update profile
	3. modify the information.
	4. click save

	<update nurse>
	1. hit Hospitals, then hit view personnel
	2. under the nurses subsection click on the desired Nurse's update profile
	3. modify the information.
	4. click save

<transferee personnel>
	1. hit Hospitals, then hit view personnel
	2. Click Remove personnel by the desired person 

	<remove personnel>
	1. hit Hospitals, then hit view personnel
	2. Click Move personnel by the desired person
	3. click the Delete this

	<view Patients>
	1. hit Hospitals, then hit view Patients

	<view specific patient>
	1. hit Hospitals, then hit view Patients
	2. Hit View Details

	<transfer patient>
	1. hit Hospitals, then hit view Patients
	2. Hit View Details
	3. Hit Transfer at the bottom left of the page

	<View medical history>
	Note: this is only if there is medical history for that patient
	1. hit Hospitals, then hit view Patients
	2. Hit View Details
	3. Hit View at the bottom right of the page

	<give a patient a prescription>
	1. hit Hospitals, then hit view Patients
	2. Hit View Details
	3. hit add a proscription on the bottom left of the page
	4. Fill out the form
	5. click send

<Root Function>

	Now that we have cover basic user functions lets do Admin things
	
	<View log>
	1. Do the login step but this time use the username: admin with the password:admin
	2. Hit "system"
	3. Then under the system drop down hit Log
	4. You should now be seeing the log of the entire system.
	
	<filter Log> 
	1. Hit "system"
	2. Then under the system drop down hit Log
	3. You should now be seeing the log of the entire system.
	4. In the upper left there is a blue word filter, hit that 
	5. enter the dates and hit filter
	6. You should now see the filtered log

	<View Stats>
	1. Hit "system"
	2. Then under the system drop down hit statistics
	3. You should now be seeing the log of the entire system.

	<Filter Stats>
	1. Hit "system"
	2. Then under the system drop down hit statistics
	3. You should now be seeing the stats of the entire system.
	4. In the upper left there is a blue word filter, hit that 
	5. Enter the dates and select a hospital.
	6. Hit filter and you should now see the filtered statistics

	<create hospital>
	1. hit Hospitals, then hit hospitals
	2. At the very top hit Create Hospital
	3. Fills out the information.
	4. Then hit Create.

	<modify hospital>
	1. hit Hospitals, then hit hospitals
	2. Click Edit on the hospital you want to edit
	3. Modify what information you want to edit.
	4. Click save

	<delete hospital>
	1. hit Hospitals, then hit hospitals
	2.click Delete on the hospital you want to delete
	3. hit the delete confirmation

	<create doctor>
	1. hit Hospitals, then hit create Doctor
	2. Fill out fields 
	3. click register

	<create Nurse>
	1. hit Hospitals, then hit create Nurse
	2. Fill out fields 
	3. click register

	<update doctor>
	1. hit Hospitals, then hit view personnel
	2. under the doctors subsection click on the desired doctor's update profile
	3. modify the information.
	4. click save

	<update nurse>
	1. hit Hospitals, then hit view personnel
	2. under the nurses subsection click on the desired Nurse's update profile
	3. modify the information.
	4. click save

	<create admin>
	1. hit Hospitals, then hit create admin
	2. Fill out fields 
	3. click register

	<update admin>
	1. hit Hospitals, then hit view personnel
	2. under the administrators subsection click on the desired admin's update profile
	3. modify the information.
	4. click save

	<transferee personnel>
	1. hit Hospitals, then hit view personnel
	2. Click Remove personnel by the desired person 

	<remove personnel>
	1. hit Hospitals, then hit view personnel
	2. Click Move personnel by the desired person
	3. click the Delete this

	<view Patients>
	1. hit Hospitals, then hit view Patients

	<view specific patient>
	1. hit Hospitals, then hit view Patients
	2. Hit View Details

	<transfer patient>
	1. hit Hospitals, then hit view Patients
	2. Hit View Details
	3. Hit Transfer at the bottom left of the page

	<View medical history>
	Note: this is only if there is medical history for that patient
	1. hit Hospitals, then hit view Patients
	2. Hit View Details
	3. Hit View at the bottom right of the page

	<give a patient a prescription>
	1. hit Hospitals, then hit view Patients
	2. Hit View Details
	3. hit add a proscription on the bottom left of the page
	4. Fill out the form
	5. click send

	<View Inbox>
	1. Hit �View your Messages� under Messaging at the to of the page.
	2. Now you should be seeing your entire in box.

	<View Sent messages>
	1. Hit �View your sent Messages� under Messaging at the to of the page.
	2. Now you should be seeing your sent box.

	<Sending a Message>
	1. Hit �Send a Message� under Messaging at the to of the page.
	2. choose the recipaint from the drop down and the top left.
	3. Then fill in the subject just under the drop down.
	4. Next fill in your message under the Body field.
	5. Lastly hit send, you should be prompted with a confirmation saying that the message was sent.

	<Replying to a Message>
	1. Hit �View your Messages� under Messaging at the to of the page.
	2. Now you should be seeing your entire in box.
	3. Click reply under one of the received messages
	4. Next fill in the body under the subject line.
	5. Lastly hit send at the bottom right of the page.

	<getting to the dango admin panel>
	1. Log in as root
	2. click Admin Interface at the top of the page.

#bugs and disclaimers#


#Known missing features#

	
