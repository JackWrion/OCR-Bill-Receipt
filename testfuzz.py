from thefuzz import fuzz

sample = '“*"*Thank You. Please Come Again.'
sample2 = "****THANK YOU. PLEASE COME AGAIN.****"
sample3 = "****Thank You. Please Come Again.****"

print (fuzz.ratio(sample.lower(), sample2.lower()))
print (fuzz.ratio(sample3.lower(), sample2.lower()))