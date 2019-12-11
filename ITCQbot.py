import praw
import pdb
import re
import os
import datetime
from praw.exceptions import APIException


USER_AGENT = "raspi:dont_step_on_snek:v1.0.0"

if not os.path.isfile("/home/pi/piITCQbot/posts_replied_to.txt"):
	posts_replied_to = []
else:
	with open("posts_replied_to.txt", "r") as f:
		posts_replied_to = f.read()
		posts_replied_to = posts_replied_to.split("\n")
		posts_replied_to = list(filter(None, posts_replied_to))

if not os.path.isfile("/home/pi/piITCQbot/comments_replied_to.txt"):
	comments_replied_to = []
else:
	with open("comments_replied_to.txt", "r") as g:
		comments_replied_to = g.read()
		comments_replied_to = comments_replied_to.split("\n")
		comments_replied_to = list(filter(None, comments_replied_to))

if not os.path.isfile("/home/pi/piITCQbot/posts_replied_to.txt"):
        skip_these = []
else:
        with open("skip_these.txt", "r") as h:
                skip_these = h.read()
                skip_these = skip_these.split("\n")
                skip_these = list(filter(None, skip_these))



reddit = praw.Reddit(client_id='xEyS3enAQSD6Bg',
                   client_secret='0gmMdcJHB9IMWaPMTy_aJdizP1k',
                   username='ITCQbot',
                   password='Pass2019',
		   user_agent='USER_AGENT')

wordArr = ["high school", "getting started", "beginner", "noob","switch to it","switching to it","where do i start","entry-level","entry level",]

networking = """Hello, please see below for a list of homelab projects based on category, each list increasing in difficulty under each section. Homelabbing is incredibly important!
\n **Networking**
* Identify your local subnet, then navigate to the gateway, e.g. [192.168.1.1](https://192.168.1.1) \- Change your default passwords and disable remote administration.
* Become familiar with your routers interface and control panel by creating DENY rules for insecure protocols like Telnet on port 23.
* Buy a Unifi WAP, and install the Unifi Controller on any machine, configure the WAP to server Wifi in addition to your SOHO router.
* Buy a Unifi CloudKey to get the controller off your gaming rig. Become familiar with the Unifi Controller interface. You could also install it on a Raspberry Pi.
* If your router supports it, create VLANs to separate your infrastructure and workstations. Cloudkey/RasPi and your smart phones/gaming rigs/laptops should be separate. If your router does not support it, pick up a managed switch (being sure to account for licensing/noise/power draw/size) and adopt it into your Unifi controller, if it is Unifi.
* Change your subnet from the ill-advised [192.168.1.0/24](https://192.168.1.0/24) subnet to something like to facilitate VPN routing, which we will see later. Changing the third octet is the best way to do this.
* Purchase a Unifi USG or any other enterprise-grade router (being sure to account for licensing/noise/power draw/size), and configure your network behind it. Adopt it into your Unifi controller.
* Become familiar writing firewalls rules to this firewall. Set up your VLANs again, if you didn't get a managed switch, and take advantage of QoS for video game traffic and any of the other neat features.
* Configure a Guest WiFi and a "Captive Portal" to keep visitor devices away from your internal network in the Unifi Controller.
* Certs to study for while labbing:  CompTIA Net+, Cisco CCNA, Cisco CCNP

^To see more, try replying to this with: `IDEAS: networking`, or replace `networking` with `severs, sysadmin, coding, scripting, security, cloud`"""

servers = """Hello, please see below for a list of homelab projects based on category, each list increasing in difficulty under each section. Homelabbing is incredibly important!
\n **Services and Servers**
* Pick up a Raspberry Pi with a PSU, a case, and a MicroSD and install the standard Raspian Buster on it. Learn the basics of Linux installation, and how root directories work.
* Turn this RasPi into your DNS PiHole. Follow any of the widely available guides and set this thing up to block all ad traffic to your network. Exceptions can be made if you find it too restrictive.
* On that same RasPi, set up an OpenVPN server to act as a VPN back to your network. Create a profile for your devices and check that the VPN subnet doesn't conflict with your internal subnet.
* On that same RasPi, attach an external hard drive by USB. Configure SMB through Samba to allow other devices on your LAN to save files to that external hard drive.
* Seeing that your Pi may now be overworked, stack some pennies on top of the CPU if your kit didn't come with a heatsink, and pick up an old Optiplex or PowereEdge. Homeserver hardware does NOT need to be new or cutting edge. Install any Debian based server distro, or CentOS 7. Here, reconfigure Samba, leaving PiHole and OpenVPN on the RasPi.
* On this Linux server, install Plex, Kodi, Emby, or Jellyfin for media management. Use your external storage, or pick up some HDDs. These can be configured into a mdadm RAID on Linux, but I do not suggest this until you get much more familiar with Linux.
* Here, read:  *The Linux Command Line by William Shotts*. You will only need to get a few chapters in before you become really comfortable.
* Using DVRs like Sonarr, Radarr, Jacket, Deluge, or others, configure your server to (legally) source media. Or just use a USB 3.0 DVD/BluRay reader to collect BRips of your movies. Configure port forwarding on your router so that your library is available to your friends and family.
* Another RasPi, with an external hard drive, and an OpenVPN profile, can be placed on your parent's or friend's network for offsite backups. Configure this with `rsync` or `librsync` to remotely backup all of your .conf files for all the various services on your servers. If a bolt of lightning ever melts your entire network, re-building would be easy with these backed up off-site.
* Using an nginx reverse proxy, configure remote access to Ombi on either a free or paid registered domain. use DNS A Name records to point towards your network from the internet, and consider a Dynamic DNS service if your IP changes often.
* Use that same nginx reverse proxy to create a sub-domain for the web interface of an Nextcloud instance, which you can use to sync files and photos from all your devices, including smart phones. Use this to replace the obsolete Samba service.
* Pick up a NAS or build one yourself for automated backups of your media and files. Drives do fail.
* IMPORTANT: Either virtualize your server, or create a virtual environment on that server where you can create your lab. Some people even pickup entirely separate hardware since labbing can be dangerous for production servers. Install VMs for LDAP services, workstation nodes, pentesting, etc. Having a true virtualized lab is the most important thing you can do for your learning.
* Certs to study for while labbing: Comptia A+, CompTIA Linux+, Red Hat RHCSA

^To see more, try replying to this with: `IDEAS: networking`, or replace `networking` with `severs, sysadmin, coding, scripting, security, cloud`"""


coding = """Hello, please see below for a list of homelab projects based on category, each list increasing in difficulty under each section. Homelabbing is incredibly important!
\n **Coding**
* Enroll in some free Python course from MIT OpenCourseWare or Coursera or Codecademy. Learn the basics of loops, lists, variables. Learn not only how to write [HelloWorld.py](https://HelloWorld.py), but also how to call and execute it. Python3 works on both Windows and \*nix.
* Read: *Automate the Boring Stuff with Python by Al Sweigart.* This book is aimed at IT people, not development people. Work your way through this book and do not skip any of the labs or exercises at the end of each chapter.
* Create a GitHub or GitLab account.
* Create a Reddit bot, just like me! Host it on your RasPi. Post the source code on your GitHub.
* Create a script that can reorganize files by file name, so facilitate media management on your media server. Something like:  `Adventure Time Season 8 Episode 7 - The Invitation.mkv` \--> `Adventure_Time_S08E07.mkv`. Post the source code on your GitHub.
* Using Flask, create a locally-hosted webapp on your RasPi that will randomly assign weekly chores to all the members of your house. Use your coding skills to make sure that you never get assigned to bathroom duty. Post the source code on your GitHub.
* Pull down an open source Python project from GitHub, and use PyUnit to write some unit tests. Submit the tests to the repo owner, and the results, and if he/she makes those fixes, pin that repo to your profile, since you are now an official contributor to FOSS projects.
* Build up your skills by focusing into a niche. You can combine Python with SQL to practice Data Science, or use Python for PenTesting/Hacking. Combine it with Bash and Powershell for systems administration or DevOps. It can also be used for straight software dev. You will need to dedicate some time to Bash, Powershell, SQL, or any other supplemental language to be able to use them effectively.
* Read either: *Learn Powershell in a Month of Lunches by Don Jones & Jeffery Hicks*  \- or -  *Learning the Bash Shell by Cameron Newham*  \- or -  *Learning SQL by Alan Beaulieu.* You will need to dedicate almost equal effort to learning these other languages in order to be effective at it.
* Certs to study for while labbing: Python Institue PCEP, Python Institute PCAP,  Microsoft Certified Azure Data Scientist Associate , AWS Big Data Specialty

^To see more, try replying to this with: `IDEAS: networking`, or replace `networking` with `severs, sysadmin, coding, scripting, security, cloud`"""

scripting = """Hello, please see below for a list of homelab projects based on category, each list increasing in difficulty under each section. Homelabbing is important!
**Scripting**
* Enroll in some Powershell or Bash courses from Codecadamy or Udemy. Learn the basics of the commands and how the shell interacts with the operating system.
* Read either: *Learn Powershell in a Month of Lunches by Don Jones & Jeffery Hicks*  \- or -  *Learning the Bash Shell by Cameron Newham.* These books are generally considered the best for beginners to these languages. Work your way through one of these books, depending on your current job and which job you want to have, and do not skip any of the labs or exercises at the end of each chapter.
* Create a GitHub or GitLab account.
* Automate the creation of a new account in an LDAP server. Have it such that you only need 2 fields for the entire account creation. Such as full name, and job title. Using string manipulation, split the `fullname` string at the first space, accounting for names that start with "Van" or "St" of "Di", and use those two new strings to create an email account as per your naming convention, the account name, SAMAccountName, add that member to groups based on the contents of the `job_title` field. Create a Home drive (H:) and auto-map it to the users, and make it such that only the domain admin and the user can access that folder. The goal is to have the process be as automated as possible.
* Do the same for account removals. And then create a Powershell / Bash script that can be used to automatically pull updates, allow you to deselect any available ones that may break anything, and then reboot itself at a certain time/day of the month.
* Certs to study for while labbing: Microsoft MCSA Server 2016, Azure AZ-103, AZ-3

^To see more, try replying to this with: `IDEAS: networking`, or replace `networking` with `severs, sysadmin, coding, scripting, security, cloud`"""

sysadmin = """Hello, please see below for a list of homelab projects based on category, each list increasing in difficulty under each section. Homelabbing is incredibly important!
\n **Systems Administration**
* In your Lab VM host, create an Active Directory forest on an unlicensed Windows Server 2012 or 2016 machine for all the machines on your home network, and a few stray Win7 and Win10 nodes that are also virtualized. Join these devices to the domain.
* Use Group Policy to manipulate settings and config and block certain behaviors like USB drive execution, and block Powershell for all devices. Create OUs for devices, users, and service users. Set policies for account lockouts, password complexity requirements, and Home (H:) drive mappings.
* Set up a nested ESXi host, on the VM host you are currently working on, on the same level as the DC.
* Create a wiki on IIS7 or otherwise, and start generating documentation and SOPs about account creation, infrastructure diagrams, and groups.
* Create a WDS server to facilitate deployments of new machines, either virtualized or otherwise. Make this image such that you can select or deselect the installation of each app/program, which are executed in an order through their .msi with different flags for different things. Go so far as to configure the desktop and display settings, all off the same .wim file starting point. Document this as well.
* Certs to study for while labbing: Microsoft MCSA Server 2016,  MSCA SQL Server, MCSE: Mobility

^To see more, try replying to this with: `IDEAS: networking`, or replace `networking` with `severs, sysadmin, coding, scripting, security, cloud`"""

security = """Hello, please see below for a list of homelab projects based on category, each list increasing in difficulty under each section. Homelabbing is incredibly important!
\n **Security**
* Change the default passwords on all of your routers/switches/desktops/infrastructure
* Use `netstat` to identify all listening ports on your machines, and verify that nothing looks too fishy. Use `ufw` on Debian distros, `firewalld` on CentOS, or Windows Firewall on your network infrastructure to harden those servers. For example, an Ubuntu server with SSH, Plex, Nextcloud, Samba, and Sonarr/Radarr/DVR apps may seem like a server with a lot of open ports, but a properly configured `ufw` list would only require 10-15 allow entries, depending on config.
* Download Kali Linux onto a bootable USB drive. Break it in by running John the Ripper on an intentionally weak password with the base word in your dictionary list. e.g. Passw0rd1 -> password.
* Run nmap scans against every device on your network and pipe the output into an HTML file for review. Examine any open ports that shouldn't be open on those devices and remediate.
* Disable port-knocking on your critical infrastructure. Disable root login for SSH. Disable shell execution for service accounts.
* Run OWSAP ZAP and nikto against your wiki or your Flask app, or any website where you have permission to touch the servers. Compare the outputs of these, and if you own the servers, try to remediate.
* Use a solution list BitWarden to securely store all credentials for your sprawling homelab. This can act both as a container for those credentials and a feeder to your devices like KeePass and LastPass.
* Try to use Aircrack-ng on any vulnerable WiFi networks that you have permission to test. Use Ettercap to try to conduct a man-in-the-middle attack against one of the nodes on your virtual network. Do not be discouraged when it is much harder than it looks. Play with the rest of the tools, and then create a stable and persistent Ubuntu machine that has all these tools already calibrated to your needs, and any additional tools you may need. Kali is great, but its main benefit is portability. Having a custom-built pentesting box that is tailored for your needs will make security auditing much easier when you don't need to worry about stealth.
* Create a VM on your network that has access to all devices and use it to run OpenVAS for vulnerability scanning and management.
* Install Metasploitable machines (intentionally weak OS's to practice compromise/rooting/privesc/etc.) on your VM host and use your hacking box to break into these and compromise them.
* Create an account on BugBounty and begin launching web application vulnerability scans against BB clients.
* Certs to study for while labbing: CompTIA Sec+, CySA+, National EC Council's C|EH, OffSec's OSCP

^To see more, try replying to this with: `IDEAS: networking`, or replace `networking` with `severs, sysadmin, coding, scripting, security, cloud`"""

cloud = """Hello, please see below for a list of homelab projects based on category, each list increasing in difficulty under each section. Homelabbing is incredibly important!
\n **Cloud**
* Cloud is difficult because it is hard to be agnostic. Unless your company specifically uses one, just pick whichever you have the most access to - cloud is not cheap to practice/lab with.
* Generally, AWS for tech, Azure for businesses (due to its native O365 integration and AD integration)
* Create accounts for AWS, Azure and GCP, staggering them by months to ensure that you get the most amount of sign-up benefits for each provider
* In all three, host a couple VMs in a VNet with an NSG, Deploy monitoring and health checks to these VMs. Take snapshots of your VMs, delete the VM (or something more fun like a forkbomb, see:   `: (){ :|:$ };:`   or simply run `sudo rm -rf --no-preserve-root` or `sudo chmod -x /*`. Once you've sufficiently screwed up your VM, restore it from the snapshots.
* In Azure, create a directory similar to your On-Prem AD if you have one from the Systems Administrator section. Use the Azure Sync plugin to have directory changes synchronized between cloud and on-prem directories.
* In Azure, create blob storage and synchronize your stuff between your network and the cloud. Create a VPN to the cloud that allows you to forward other traffic besides LDAP replication between here and there.
* In Azure, create Office 365 accounts for yourself and anyone else who may need it, and integrate O365 storage and account creds with your Azure AD.
* In AWS, configure and deploy Route53 for your Nextcloud and Ombi instances on your home server from the Services and Servers section. Get this to work on IPv6 as well.
* In AWS, configure a load balancer for multiple EC2 instances, using 2 or more availability zones.
* In AWS, create a DynamoDB table and load in data, and try to retrieve it with a script, either from AWS CLI or on your local machine.
* In GCP, try to do the above.
* Certs to study for while labbing: Azure AZ-103, AZ-300,  AWS Cloud Practitioner, AWS SysAops Administrator, AWS Solutions Architect, GCP Associate Cloud Eng., GCP Professional Cloud Architect

^To see more, try replying to this with: `IDEAS: networking`, or replace `networking` with `severs, sysadmin, coding, scripting, security, cloud`"""

ideas = {"networking": networking,
              "servers": servers,
              "services": servers,
              "coding": coding,
              "scripting": scripting,
              "sysadmin": sysadmin,
              "security": security,
              "cloud": cloud
             }

github_link = "^(https://github.com/bcornw2/ITCQbot)"

subreddit = reddit.subreddit('pythonforengineers')

def main():

#    stream = praw.models.util.stream_generator(submissions_and_comments(subreddit))
   # for comment in stream.comments(skip_existing=True):
   #     if post 

#    start_time = time.time()
    while True:
        for submission in subreddit.stream.submissions(pause_after=0,skip_existing=True):
            print("  =  =  find submission")
            try:
                if submission is None:
                        print("Submission of type None")
                        break
                if submission.id not in posts_replied_to:
                    print("bot replying to submission id:  " +  submission.id)
                    with open("posts_replied_to.txt", "a") as file:
                        file.write(submission.id + "\n")
                    process_submission(submission)
                #if submission is None:
                #        break
                if submission.id in skip_these:
                    break
                else:
                    break
            except AttributeError as e:
                    print("Error! under submission : {0}".format(e))


        for comment in subreddit.stream.comments(pause_after=0,skip_existing=True):
            print("  =  =  find comment ")
            try:
                if comment is None:
                    print("Comment of type None")
                    break
            #print("  =  =  find comment ")
                if comment.id not in comments_replied_to:
                    #print("comment.author.name: " + str(comment.author.name) + " | comment.id " + comment.id + " | comment.parent().author.name: " + str(comment.parent().author.name))
                    with open("comments_replied_to.txt", "a") as file:
                        file.write(comment.id + "\n")
                    if((str(comment.author.name) != "ITCQbot" and str(comment.parent().author.name) == "ITCQbot")):
                        process_reply(comment)
                    else:
                        with open("skip_these.txt", "a") as file:
                            file.write(comment.id + "\n")
                        break
                if comment.id in skip_these:
                    break
                else:
                    break
            except AttributeError as e:
                print("Comment Error!: {0}".format(e))
 #               if comment is None:
  #                  print("Comment of type None")
   #                 break
    #            if comment.id not in comments_replied_to:
     #               if((str(comment.author.name) != "ITCQbot") and (str(comment.parent().author.name) == "ITCQbot")):
      #                  process_reply(comment)
       #                 print("comment.author: " + str(comment.author.name))
        #                print("  =  =  finding comment: " + comment.id)
         #               reddit.inbox.mark_read(comment)
          #          else:
           #             break
 #               if comment is None:
#                        print("Comment of type None")
  #                      break
       #         else:
        #            break
         #   except APIException as e:
          #      print("Error! under comment : {0}".format(e))

def process_submission(submission):
    now = datetime.datetime.now()
    foundArr = []
    normalized_selftext = submission.selftext.lower()
    if len(submission.title.split()) > 15:
        return

    #populate foundArr array
    for w in wordArr:
        if w in normalized_selftext:
            foundArr.append(w)

    message=("Your post contained the words: " + str(foundArr) + ", which may mean you are just beginning your IT career journey, and are seeking advice. It is commonly suggested that people new to IT get the [CompTIA A+ certification](https://comptia.org/certifications/a), even if you think it looks too easy. While studying for this, start working on personal projects like securing your home network or building a NAS out of a RasPi - check /r/homelab and /r/raspberrypi for more ideas, or reply to this comment with:  \"IDEAS:\" `<topic>` and I will reply a list of beginner-friendly home-lab project ideas to help you learn the basic of networking, security, sysadmin, coding, and other IT topics. Once you get the A+, and have a reliable understanding of how computers work, make a resume and post it in the resume thread. Then, send out your resume to any company looking for Helpdesk, Desktop Support, Field Tech, or Tier 1 positions, for your entry into the world of IT. Be aware that your location is often the most important determining factor in IT wages and opportunities. \n If you are not, in fact, a beginner looking for getting-started advice, please tell the author of this bot that he is a failure: " + github_link)

    if len(foundArr) >= 2:
        #execute submission
        print(now.strftime("%Y-%m-%d %H:%M") + "Submission Title: " + submission.title + " | submission.id: " + submission.id + " | wordArr: " + str(wordArr) + " | foundArr:" + str(foundArr) + " | Match found!")
        print("				Writing comment!")
        try:
            with open("posts_replied_to.txt", "a") as file:
                file.write(submission.id + "\n")
            with open("logfile.txt", "a") as log:
                log.write(now.strftime("%Y-%m-%d %H:%M") + "Submission ID: " + submission.id + "Comment Body: " + submission.selftext + "\n Reply: " + message + "\n ================================== \n")
            submission.reply(message)
            print("SUBMISSION IS: " + str(submission.title))
            print(" :: SUBMISSION REPLY SENT :: ")
        except APIException as e:
                    print("error!: {0}".format(e))
    else:
        with open("skip_these.txt", "a") as file:
                file.write(submission.id + "\n")
#        print(now.strftime("%Y-%m-%d %H:%M") + "Submission Title: " + submission.title + " | submission.id: " + submission.id + "|  foundArr:" + str(foundArr) + " | foundArr found less than 3 matches, not commenting.")
        print("  =  =  Not commenting.")


def process_reply(comment):
    now = datetime.datetime.now()
#    if comment.id not in comments_replied_to:
    normalized_replytext = comment.body.lower()
    word0 = normalized_replytext.split()[0]
    word1 = normalized_replytext.split()[1]
    try:
        print("word0: " + word0 + " | word1: " + word1 + " | comment.author.name: " + str(comment.author.name) + " | comment.parent().author.name: " + str(comment.parent().author.name))
    except AttributeError as e:
        print("AttributeError!: {0}".format(e))

    if (("ideas" in word0) and (str(comment.author.name) != "ITCQbot") and (str(comment.parent().author.name) == "ITCQbot")):
            print("made it to triple if statement")
            if word1 in ideas:
                messageReply = ideas[word1]
                comment.reply(messageReply)
                print("COMMENT IS: " + comment.body + " | MESSAGE IS: " + messageReply)
                print(" :: MESSAGE REPLY SENT :: " + messageReply)
                with open("comments_replied_to.txt", "a") as file:
                    file.write(comment.id + "\n")
                with open("logfile.txt", "a") as log:
                    log.write(now.strftime("%Y-%m-%d %H:%M") + " | comment.id: " + comment.id + "comment Body: " + comment.body + "\n Reply: IDEAS[" + word1 + "]\n ================================== \n") 
            else:
                comment.reply("You can reply to this message with the following format for ideas:  `IDEAS: networking`  \n    Try one of the following categories: \n * Networking \n * Servers \n * Services \n * Security \n * Coding \n * Scripting \n * Cloud")
                with open("comments_replied_to.txt", "a") as file:
                    file.write(comment.id + "\n")


    elif((str(comment.author) is "ITCQbot") or (word1 is "can")):
        with open("comments_replied_to.txt", "a") as file:
            file.write(comment.id + "\n")
        print(" == IGNORING: NO COMMENT WRITTEN! == ")
        return
    else:
        comment.reply("You can reply to this message with the following format for ideas:  `IDEAS: networking`  \n    Try one of the following categories: \n * Networking \n * Servers \n * Services \n * Security \n * Coding \n * Scripting \n * Cloud \n")
        with open("comments_replied_to.txt", "a") as file:
            file.write(comment.id + "\n")


#def submissions_and_comments(subreddit):
#    results = []
#    results.extend(subreddit.new())
#    results.extend(subreddit.comments())
#    results.sort(key=lambda post: post.created_utc, reverse=True)
#    return results

if __name__ == '__main__':
    main()
