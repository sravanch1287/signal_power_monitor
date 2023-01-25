sudo add-apt-repository -y ppa:ettusresearch/uhd
sudo add-apt-repository -y ppa:johnsond-u/sdr


for thing in $*
do
    case $thing in
        gnuradio)
            sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gnuradio python3-gi gobject-introspection gir1.2-gtk-3.0 python3-cairo python3-gi-cairo
            ;;

        srslte)
            sudo DEBIAN_FRONTEND=noninteractive apt-get install -y srslte
        sudo apt-get update;
        sudo apt-get install python3-pip;
        pip3 install -r requirements.txt;
        ;;
    esac
done

sudo apt-get update
echo "echo apt-get update ran" >> ~/.bashrc 
sudo apt-get -y install python3-pip
echo "echo pip3 installed" >> ~/.bashrc 
sudo pip3 install -r requirements.txt
echo "echo installed required packages" >> ~/.bashrc 
sudo apt-get -y install gnuradio
echo "echo installed gnuradio" >> ~/.bashrc 
sudo apt-get -y install libatlas-base-dev
echo "echo installed libatlas" >> ~/.bashrc 
sudo pip3 install -r requirements.txt
echo "echo installed requirements.txt" >> ~/.bashrc 

sudo sysctl -w net.core.rmem_max=24862979
sudo sysctl -w net.core.wmem_max=24862979

sudo rm /usr/bin/uhd_rx_cfile
chmod +x /local/repository/uhd_rx_cfile
sudo mv /local/repository/uhd_rx_cfile /usr/bin/

chmod +x /local/repository/uhd_rx_powerfile
sudo mv /local/repository/uhd_rx_powerfile /usr/bin

chmod +x /local/repository/iq_to_power.py
sudo mv /local/repository/iq_to_power.py /usr/bin/

chmod +x /local/repository/bin_avg.py
sudo mv /local/repository/bin_avg.py /usr/bin/

chmod +x /local/repository/uhd_siggen_timing
sudo mv /local/repository/uhd_siggen_timing /usr/bin/

chmod +x /local/repository/uhd_siggen_45sec
sudo mv /local/repository/uhd_siggen_45sec /usr/bin/

chmod +x /local/repository/uhd_siggen_90sec
sudo mv /local/repository/uhd_siggen_90sec /usr/bin/


chmod +x /local/repository/cir_tx.py
sudo mv /local/repository/cir_tx.py /usr/bin/

chmod +x /local/repository/cir_rx8d.py
sudo mv /local/repository/cir_rx8d.py /usr/bin/

chmod +x /local/repository/cir_rx9d.py
sudo mv /local/repository/cir_rx9d.py /usr/bin/

chmod +x /local/repository/cir_rx10d.py
sudo mv /local/repository/cir_rx10d.py /usr/bin/

chmod +x /local/repository/pdp_analysis.py
sudo mv /local/repository/pdp_analysis.py /usr/bin


sudo ed /etc/sysctl.conf << "EDEND"
a
net.core.rmem_max=24862979
net.core.wmem_max=24862979
.
w
EDEND

#sudo "/usr/lib/uhd/utils/uhd_images_downloader.py -t x310"
