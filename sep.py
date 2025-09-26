input_file = "input.txt"
output_file = "output.txt"

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        items = line.strip().split(",")
        for item in items:
            outfile.write(item.strip() + "\n")
