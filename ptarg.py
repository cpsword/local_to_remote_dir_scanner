import optparse
import Queue
import threading
import os
import urllib2

def parse_args():
    parser = optparse.OptionParser('usage:%prog -u targer_url -d local_dir')
    parser.add_option('-t','--threads',dest='threads',type='int',default=5,help='set the threads to scan')
    parser.add_option('-d','--dir',dest='directory',type='string',help='set local directory to compare with remote directory')
    (options,args) = parser.parse_args()
    if len(args) < 1:
        paser.print_help()
        sys.exit(0)
    return options,args

def get_web_paths(directory):
    filters = [".jpg",".gif",".png",".css"]
    os.chdir(directory)
    web_paths = Queue.Queue()
    for r,d,f in os.walk('.'):
        for files in f:
            remote_path = "%s/%s" % (r,files)
            if remote_path.startswith("."):
                remote_path = remote_path[1:]
            if os.path.splitext(files)[1] not in filters:
                web_paths.put(remote_path)
    return web_paths

def test_remote(web_paths,domain):
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s" % (domain,path)
        headers={'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:73.0) Gecko/20100101 Firefox/73.0'}
        request = urllib2.Request(url,headers=headers)
        try:
            response = urllib2.urlopen(request)
            print "[%d] => %s" % (response.code,path)
            response.close()
        except urllib2.HTTPError as error:
            if hasattr(error,'code'):
                print "[%d] => %s" % (error.code,path)
            pass

if __name__ == '__main__':
    directory = parse_args()[0].directory
    threads = parse_args()[0].threads
    domain = parse_args()[1][0]
    web_paths = get_web_paths(directory)
    test_remote(web_paths,domain)
    #for i in range(threads):
    #    print "Spawning thread: %d" % i
    #    t = threading.Thread(target=test_remote,args=(web_paths,domain))
    #    t.start()
