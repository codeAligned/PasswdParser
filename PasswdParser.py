import os,sys,json,warnings

#class to parse passwd
class PasswdParser():
    def __init__(self,sysargv):
        #Take input file paths as agrument, defaulting to the standard system path.
        passwd_path, group_path = '/etc/passwd','/etc/group'
        #if 2 arguments are passed
        if (len(sysargv)-1 == 2):
            passwd_path, group_path = sys.argv[1:]
        #check if input files are present
        passwd_exists, group_exists = self.fileExists(passwd_path), self.fileExists(group_path)
        #parse passwd 
        if(passwd_exists and group_exists):
            self.parsePasswd(passwd_path, group_path)

    #Function to parse passwd
    def parsePasswd(self, passwd_path, group_path):
        #Read files from the respective paths
        passwd_file, group_file = self.readFile(passwd_path), self.readFile(group_path)
        user_group_map, groups_map = self.getGroupDetails(group_file)
        passwd_parser = self.getPasswdParser(passwd_file, user_group_map, groups_map)
        passwd_parser_json = json.dumps(passwd_parser, indent = 4, sort_keys = True)
        print(passwd_parser_json)
        #put result in json file in the current directory
        self.saveJson(passwd_parser)
        sys.exit(0)

    #Function to create username => {"uid", "full_name", "groups"} mapping
    def getPasswdParser(self, passwd_file, user_group_map, group_map):
        passwd_map = {}
        for user in passwd_file:
            user_details = user.split(':')
            if user.startswith('#'):
                pass
            elif(len(user_details) == 7):
                username = user_details[0]
                uid = user_details[2]
                gid = user_details[3]
                full_name = user_details[4]
                group_list = []

                for group in user_group_map.get(username,[]):
                    group_list.append(group)
                group_list.append(group_map.get(gid,None))
                passwd_map[username] = {"uid" : uid, "full_name" : full_name, "groups" : group_list}
            else:
                warnings.warn("Line number ", i, "is malformed in file ", passwd_file)
        return passwd_map

    #Funtion to create:
    # 1. User => List of group_name mapping
    # 2. gid => group_name mapping
    def getGroupDetails(self, group_file):
        user_group_map = {}
        groups = {}
        for i, group in enumerate(group_file):
            group_details = group.split(':')
            if group.startswith('#'):
                pass
            elif len(group_details) == 4:
                group_name = group_details[0]
                gid = group_details[2]
                user_list = group_details[3]
                groups[gid] = group_name
                for user in user_list.split(','):
                    user_group_map.setdefault(user, []).append(group_name)
            else:
                warnings.warn("Line number ", i, "is malformed in file ", group_file )
        return user_group_map, groups

    #Check if file path is valid
    def fileExists(self, path):
        if not os.path.isfile(path):
            raise Exception(path, 'file not present')
        return True

    #Read file at path into list of lines 
    def readFile(self, path):
        try: 
            with open(path) as f:
                try:
                    _file = f.readlines()
                except Exception as exp:
                    raise Exception(path, 'file is malformed')
        except:
            raise Exception('Cannot open file at : ' , path)
        return _file

    #Save json result in the file './passwd_parser.json'
    def saveJson(self, json_result):
        try:
            with open('passwd_parser.json', 'w', encoding='utf-8') as f:
                json.dump(json_result, f, ensure_ascii=False, indent=4)
        except:
            print('Cannot save the JSON in file in the current directory')

if __name__ == "__main__":
    PasswdParser(sys.argv)