import re

class DHCP:
    def __init__(self, request):
        for line in request.splitlines():
            if "ff:ff:ff:ff:ff:ff" in line:
                self.mac = self.__matchMac(line)
            elif "Hostname" in line:
                self.name = self.__matchName(line)
        if not self.name:
            self.name = "Unknown User"
            
    def __init__(self):
        pass
    
    def __matchMac(self, string):
        mac = re.findall("(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})", string)[0][0]
        return mac

    def unittest_matchMac(self):
        mac_address = self.__matchMac("15:07:44.524519 34:e6:d7:43:c9:6c > ff:ff:ff:ff:ff:ff, ethertype IPv4 (0x0800), length 342: (tos 0x0, ttl 128, id 1911, offset 0, flags [none], proto UDP (17), length 328)")
        #return mac_address == "34:e6:d7:43:c9:6c"
        return mac_address
    
    def __removeSuffix(self, interest_char, subject):
        final_index = subject.rfind(interest_char)
        return subject[:final_index]

    def unittest_removeSuffix(self):
        suffix_less = self.__removeSuffix("s",  "willsiphone")
        # suffix_less == "will"
        return suffix_less
    
    def __handleDashSuffix(self, hostname):
        # Dash Delimited
        if "-" in hostname:
            return self.__removeSuffix("-", hostname)
        return hostname

    def unittest_handleDashSuffix(self):
        dash_less = self.__handleDashSuffix("will-iphone")
        # return dash_less == "will"
        return dash_less
        
    def __handleMultiName(self, hostname):
        if not hostname.isupper():
            first_name = re.findall('[A-Z][^A-Z]*', hostname)[0]
            return first_name
        return hostname

    def unittest_handleMultiName(self):
        first_name = self.__handleMultiName("WillHeld")
        # return first_name == "Will"
        return first_name
    
    def __handleApple(self, hostname):
        hostname = self.__handleDashSuffix(hostname)
        
        # Possesive Case
        possesive_instances = ["sipad", "siphone", "smbp", "sair", "s"]
        if any(hostname.lower().endswith(possesive_instance) for possesive_instance in possesive_instances):
            hostname = self.__removeSuffix("s", hostname)

        # Handle Multiple Names
        name = self.__handleMultiName(hostname)
        return name
    
    def __handleWindows(self, hostname):
        # Dashed Suffix
        hostname = self.__handleDashSuffix(hostname)
        
        # Handle Multiple Names
        name = self.__handleMultiName(hostname)
        return name
    
    def __matchName(self, string):
        print(string)
        hostname = re.findall('".+"', string)[0].replace('"', '')
        print(hostname)
        apple_names = ["mbp", "iphone", "ipad", "air"]
        windows_names = ["pc"]
        # If the device is an apple device
        if any(apple_name in hostname.lower() for apple_name in apple_names):
            name = self.__handleApple(hostname)
            # If the device is a windows device
        elif any(windows_name in hostname.lower() for windows_name in windows_names):
            name = self.__handleWindows(hostname)
        if name:
            return name
        else:
            return "Unknown User"
        
