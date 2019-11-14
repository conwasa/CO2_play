i"# CO2_play" 
"#CO2"
Playing with a way to render back-end data using Google Storage, Handlebars and Google's visualisation API, as a precursor to useing those things on another project.

The Pyrhon was written on a Windows 7 system with Python 3.7.1. The development Linux system had verson 3.5. Production (an old laptop with an Intel Duo processor).

To upgrade production to Phython 3.7.1:

wget https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tgz
tar -xvf Python-3.7.1.tgz
cd Python-3.7.1
sudo ./configure --enable-optimizations
sudo make -j8
sudo make install

zipimport.ZipImportError: can't decompress data; zlib not available
sudo apt install lib64z1
sudo make install



 
