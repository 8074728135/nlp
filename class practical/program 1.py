import re

text = """Rahul contacted me at 9876543210 and his email is rahul@gmail.com
Priya can be reached at 8765432109, email priya@yahoo.com
Arun's phone is 9988776655 and mail is arun@outlook.com
Meena called from 9123456780, email meena@gmail.com
Karthik: 8899776655, karthik@yahoo.com
Divya: 9345678901, divya@outlook.com
Vijay: 9786543210, vijay@gmail.com
Anjali: 8877665544, anjali@yahoo.com
Ravi: 9090909090, ravi@gmail.com
Sneha: 9867543210, sneha@outlook.com

Ajay: 9001122334, ajay@gmail.com
Neha: 9112233445, neha@yahoo.com
Suresh: 9223344556, suresh@outlook.com
Pooja: 9334455667, pooja@gmail.com
Manoj: 9445566778, manoj@yahoo.com
Lakshmi: 9556677889, lakshmi@outlook.com
Ramesh: 9667788990, ramesh@gmail.com
Kavya: 9778899001, kavya@yahoo.com
Dinesh: 9889900112, dinesh@outlook.com
Swathi: 9990011223, swathi@gmail.com

Harish: 9011223344, harish@yahoo.com
Nandini: 9022334455, nandini@gmail.com
Gokul: 9033445566, gokul@outlook.com
Deepa: 9044556677, deepa@yahoo.com
Mohan: 9055667788, mohan@gmail.com
Aishwarya: 9066778899, aishwarya@outlook.com
Surya: 9077889900, surya@gmail.com
Keerthi: 9088990011, keerthi@yahoo.com
Prakash: 9099001122, prakash@outlook.com
Shalini: 9100112233, shalini@gmail.com

Vignesh: 9122113344, vignesh@yahoo.com
Divakar: 9133224455, divakar@gmail.com
Swetha: 9144335566, swetha@outlook.com
Naveen: 9155446677, naveen@yahoo.com
Bhavya: 9166557788, bhavya@gmail.com
Lokesh: 9177668899, lokesh@outlook.com
Varun: 9188779900, varun@gmail.com
Harini: 9199880011, harini@yahoo.com
Sanjay: 9200991122, sanjay@outlook.com
Pavithra: 9211002233, pavithra@gmail.com

Ganesh: 9222113344, ganesh@yahoo.com
Akash: 9233224455, akash@gmail.com
Nithya: 9244335566, nithya@outlook.com
Abhishek: 9255446677, abhishek@yahoo.com
Ramya: 9266557788, ramya@gmail.com
Sathish: 9277668899, sathish@outlook.com
Monika: 9288779900, monika@gmail.com
Bala: 9299880011, bala@yahoo.com
Sowmya: 9300991122, sowmya@outlook.com
Kiran: 9311002233, kiran@gmail.com

Rohit: 9322113344, rohit@yahoo.com
Padmini: 9333224455, padmini@gmail.com
Siva: 9344335566, siva@outlook.com
Janani: 9355446677, janani@yahoo.com
Ashok: 9366557788, ashok@gmail.com
Sangeetha: 9377668899, sangeetha@outlook.com
Pradeep: 9388779900, pradeep@gmail.com
Ram: 9399880011, ram@yahoo.com
Geetha: 9400991122, geetha@outlook.com
Vasanth: 9411002233, vasanth@gmail.com

Muthu: 9422113344, muthu@yahoo.com
Preethi: 9433224455, preethi@gmail.com
Sathya: 9444335566, sathya@outlook.com
Dharani: 9455446677, dharani@yahoo.com
Bharath: 9466557788, bharath@gmail.com
Ranjith: 9477668899, ranjith@outlook.com
Uma: 9488779900, uma@gmail.com
Sridhar: 9499880011, sridhar@yahoo.com
Kavi: 9500991122, kavi@outlook.com
Anand: 9511002233, anand@gmail.com

Magesh: 9522113344, magesh@yahoo.com
Lavanya: 9533224455, lavanya@gmail.com
Dharun: 9544335566, dharun@outlook.com
Tejas: 9555446677, tejas@yahoo.com
Riya: 9566557788, riya@gmail.com
Yogesh: 9577668899, yogesh@outlook.com
Nikhil: 9588779900, nikhil@gmail.com
Ishita: 9599880011, ishita@yahoo.com
Mani: 9600991122, mani@outlook.com
Arvind: 9611002233, arvind@gmail.com

Sakthi: 9622113344, sakthi@yahoo.com
Malathi: 9633224455, malathi@gmail.com
Srinivas: 9644335566, srinivas@outlook.com
Anu: 9655446677, anu@yahoo.com
Rakesh: 9666557788, rakesh@gmail.com
Chitra: 9677668899, chitra@outlook.com
Vimal: 9688779900, vimal@gmail.com
Reshma: 9699880011, reshma@yahoo.com
Karthika: 9700991122, karthika@outlook.com
Suraj: 9711002233, suraj@gmail.com"""

phone_numbers = re.findall(r'\b\d{10}\b', text)

emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
print("PHONE NUMBERS:")
for phone in phone_numbers:
    print(phone)

print("\nEMAIL ADDRESSES:")
for email in emails:
    print(email)
