import os

directory = "/var/www/html/uploads"

for filename in os.listdir(directory):
  base = os.path.basename(filename)
  os.path.splitext(base)
  file = os.path.splitext(base)[0]
  print(filename)
