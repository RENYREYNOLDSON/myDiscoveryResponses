FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip uninstall pathlib --yes

# Copy the rest of your app's source code into the container at /app
COPY . /app/

# Run PyInstaller to compile the spec file
#RUN pyinstaller __main__.spec
CMD ["python","__main__.py"]
# Make your compile script executable
#COPY Compiler_Script.iss /app/

# Make your compile script executable
#RUN chmod +x compile.sh

# Run the compile script
#CMD ["./compile.sh"]