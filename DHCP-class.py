import re

class DHCP:
    def __init__(self, request):
        for line in request.splitlines():
            if "ff:ff:ff:ff:ff:ff" in line:
                self.MacAddress = self.__matchMac(line)
            elif "Hostname" in line:
                self.name = self.__matchName(line)
        if not self.name:
            self.name = "Unknown User"
            
    def __matchMac(self, string):
        mac = re.match("/([0-9a-fA-F]{2}[:]){5}([0-9a-fA-F]{2})/g", string)
        return mac

    def __removeSuffix(self, interest_char, subject):
        final_index = subject.rfind(interest_char)
        return subject[:final_index]

    def __handleDashSuffix(self, hostname):
        # Dash Delimited
        if "-" in hostname:
            return self.__removeSuffix("-")
        return hostname

    def __handleMultiName(self, hostname):
        
    
    def __handleApple(self, hostname):
        hostname = self.__handleDashSuffix(hostname)
        
        # Possesive Case
        possesive_instances = ["sipad", "siphone", "smbp", "s"]
        if any(hostname.lower().endswith(possesive_instance) for possesive_instance in possesive_instances):
            hostname = self.__removeSuffix("s")

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
        hostname = re.match('"\w+"', string)
        apple_names = ["mbp", "iphone", "ipad"]
        windows_names = ["pc"]
        # If the device is an apple device
        if any(appleName in hostname.lower() for apple_name in apple_names):
            name = self.__handleApple(hostname)
            # If the device is a windows device
        elif any(windows_name in hostname.lower() for windows_name in windows_names):
            name = self.__handleWindows(hostname)
        if name:
            return name
        else:
            return "Unknown User"
        
