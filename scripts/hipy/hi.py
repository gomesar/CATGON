import sys
import socket
import threading
# Crypt
from hashlib import sha256
import base64
from Crypto.Cipher import AES
from Crypto import Random
import configparser
"""
    GomesAR 2018
    [hi.py] refactored. Python 3.6.1
    
    Light **casual** communiations tool, designed to avoid internet traffic.
    Although using encryption hy.py **is not a tool for security purposes**,
    encryption has been added to hinder access to data by members of the local network itself.
    So, yes, hi.py stores sessions keys in plaintext (.cfg files).
    (hi.py also tries to fool the curious behind/beside you, discarding previous messages. [; )

    Use:

        configure your .hypi.cfg like:
            [<connection_name>]
            src_ip=0.0.0.0 #source ip
            src_port=000 # source port
            ...
            [<another_connection_name>]
            ...
        then execute passing connection_name as parameter:
            python3.6 hi.py gomes
        or use a different .cfg file:
            python3.6 hi.py gomes another.cfg

        '@q' to quit

"""

# Crypt
BS      = 16 # Block size
pad     = lambda s : s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad   = lambda s : s[:-ord(s[len(s)-1:])]
trans   = lambda k : sha256(k.encode()).digest()


def print_error(err):
    print("[!] Error.")
    print("Type: " + str( type(err) ))
    print("\t" + str( err.args ))
    print("\t" + str( err ))
    print('\tError on line {}'.format( sys.exc_info()[-1].tb_lineno ))


class Hipy():
    QUIT_CMD = "@q"
    VERSION = "1.1 (2018-03) Python3.6.1"
    HEADER = "-*- {name} {version} -*-\n{quit_instruction}".format(
            name="(hi.py)",
            version=VERSION,
            quit_instruction="Enter '{quit_cmd}' to quit.".format(
                quit_cmd=QUIT_CMD
                )
            )


    def __init__(self, cnx, cfg_file=".hipy.cfg"):
        self.src = ("0.0.0.0", 0)
        self.dst = ("0.0.0.0", 0)
        self.__key = ""
        self.__key_hash = ""
        self.__cfg_ok = self.__config(cfg_file, cnx)
        self.__quit_act = False


    def __config(self, cfg_file, cnx):
        try:
            _cfgp = configparser.ConfigParser()
            _ = _cfgp.read( cfg_file )

            _src_ip = _cfgp.get( cnx, "src_ip" )
            _src_port = int( _cfgp.get(cnx, "src_port") )

            _dst_ip = _cfgp.get(cnx, "dst_ip")
            _dst_port = int( _cfgp.get(cnx, "dst_port") )

            self.src = ( _src_ip, _src_port )
            self.dst = ( _dst_ip, _dst_port )
            self.__key = _cfgp.get( cnx, "key" ) # yes, plaintext. Remember
            self.__key_hash = trans( self.__key )
        except Exception as e:
            print_error(e)
            return False
        
        return True


    def enc(self, raw):
        try:
            _iv      = Random.new().read(AES.block_size)
            _cipher  = AES.new(self.__key_hash, AES.MODE_CBC, _iv)
    
            return base64.b64encode(_iv + _cipher.encrypt(pad(raw)) )
        except Exception as e:
            print_error(e)
            return ""


    def dec(self, cph):
        try:
            _cph_d       = base64.b64decode(cph)
            _iv          = _cph_d[:BS]
            _cipher      = AES.new(self.__key_hash, AES.MODE_CBC, _iv)

            return unpad(_cipher.decrypt(_cph_d[BS:]) )
        except Exception as err:
            print_error(err)
            return ""


    def ear(self, s):
        while 1:
            try:
                d, a = s.recvfrom(1024)
                d = self.dec(d)
                if not type(d) == str:
                    d = d.decode()

                sys.stdout.write("\033[s\n\033[K:"+d+"\033[u")
                sys.stdout.flush()
                #print " {"+d+"} "

                if d.startswith(Hipy.QUIT_CMD):
                    #print("[!] DC")
                    self.__quit_act = True
                    break;
            except Exception as e:
                print("[!] Error E")
                print_error(e)
                break


    def tongue(self, s):
        while 1:
            try:
                m = input('>')
                sys.stdout.write("\033[F\033[K")
                sys.stdout.flush()

                if m.startswith(Hipy.QUIT_CMD):
                    m = m.replace( hipy.QUIT_CMD, '@quitting    ' )
                    s.sendto( self.enc(m), self.dst )
                    print("[!] Quitting")
                    break;
                elif self.__quit_act:
                    if len(m) > 0:
                        print("[!] Connection already closed. Sorry.")
                    break;
                else:
                    s.sendto( self.enc(m), self.dst )
            except Exception as err:
                print("[!] Error T")
                print_error(err)
                break
        s.close()


    def run(self):
        """
            Creates a socket and start direct communication.
        """
    
        if not self.__cfg_ok:
            print("(hi.py) not configured.")
            sys.exit(1)

        print(Hipy.HEADER)
        try:
            _s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
            _s.bind( self.src )

            ear_h           = threading.Thread( target=self.ear, args=(_s, ) )
            ear_h.daemon    = True
            ear_h.start()

            self.tongue(_s)
        except Exception as e:
            print_error(e)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        hipy = Hipy(sys.argv[1])
    elif len(sys.argv) == 3:
        hipy = Hipy(sys.argv[1], cfg_file = sys.argv[2])
    else:
        print("Use: {} <connetion> [<cfg_file>]".format(argv[0]) )
        sys.exit(1)

    hipy.run()

