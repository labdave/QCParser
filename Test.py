from QCReport import QCReport

report = QCReport()

print report.get_sample_names()

#report.add_entry("Derp", "Herp", "Clap" ,"DISA", 2)
report.add_entry("Derp", "Herp", "Clap" ,"DISA", 2)
report.add_entry("Derp", "Herp", "Clap" ,"RICHARD", 2)
report.add_entry("Derp", "Herp", "Clap" ,"RICHARD", 2)

report.add_entry("Neville", "Herp", "Clap" ,"RICHARD", 2)
report.add_entry("Neville", "Herp", "Clap" ,"RICHARD", 2)
report.add_entry("Neville", "Herp", "Clap" ,"RICHARD", 2)

#report.add_entries("Neville", report.get_sample_data("Derp"))




print report.get_sample_names()
print report.get_sample_data("Neville")

print report.is_square()
print report.is_ordered()


print report