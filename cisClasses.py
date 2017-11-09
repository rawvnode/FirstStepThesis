import atexit

import sys
from pyVim.connect import SmartConnectNoSSL, Disconnect
import pyVmomi
from pyVmomi import vim
import inspect

class cis_2_1:
    def __init__(self, host):
        self.cis_2_1_passed = False
        configuration = host.QueryHostConnectionInfo().host.host.configManager.dateTimeSystem.dateTimeInfo.ntpConfig
        if configuration == None:
            cis_2_1_passed = False
    def __str__(self):
        return str(self.cis_2_1_passed)

class cis_2_2:
    def __init__(self, host, firewallList = list):
        self.cis_2_2_passed = False
        configuration = host.QueryHostConnectionInfo().host.host.configManager.firewallSystem.firewallInfo.ruleset
        if len(configuration) != len(firewallList):
            self.cis_2_2_passed = False
        counter = 1
        benchmark = 0#
        #for c in configuration:
        #    print(c.rule)
        #    print(len(configuration))
        ruleSetArray = len(configuration)
        ruleSet = 0
        while(ruleSet < ruleSetArray - 1):
#            print(configuration[ruleSet].rule[0])
#            print(firewallList[ruleSet].rule)
            if (configuration[ruleSet].rule[0].port == firewallList[benchmark].rule[0].port
                and configuration[ruleSet].rule[0].direction == firewallList[benchmark].rule[0].direction
                and configuration[ruleSet].rule[0].protocol == firewallList[benchmark].rule[0].protocol):
                counter = counter + 1
                benchmark = benchmark + 1
                ruleSet = -1
            ruleSet = ruleSet + 1
        if counter == ruleSetArray:
            self.cis_2_2_passed = True


    def __str__(self):
        return str(self.cis_2_2_passed)

#input:
#host: a host managed object
#used: boolean, wether SNMP is used or not
#maxTrap: int, the nmax number of allowed destinations for communications
#if SNMP is not used, it should be disabled;
#if SNMP is used, trap number and configuration should be correct
#configuration cannot be checked, the library does not extract this value
class cis_2_3:
    def __init__(self, host, used = False, maxTrap = int):
        self.cis_2_3_passed = False
        configuration = host.QueryHostConnectionInfo().host.host.configManager.snmpSystem.configuration.enabled
        if configuration == False and used == False:
            self.cis_2_3_passed = True
        elif configuration == True and used == True:
            maxTrapDestinations = host.QueryHostConnectionInfo().host.host.configManager.snmpSystem.limits.maxTrapDestinations
            if maxTrapDestinations == maxTrap:
                self.cis_2_3_passed = True
    def __str__(self):
        return str(self.cis_2_3_passed)

#input
#logDirKey: a vim.option.OptionValue managed object
#datastore: the name of the non-persistent datastore folder the logDir is in
#if the word is in the path, cis is not passed
class cis_3_2:
    def __init__(self, logDirKey, datastore = str):
        self.cis_3_2_passed = False
        if 'scratch' in logDirKey.value:
            self.cis_3_2_passed = False
        else:
            self.cis_3_2_passed = True
    def __str__(self):
        return str(self.cis_3_2_passed)

#input:
#logDirKey: a vim.option.OptionValue managed object
#server: the name of the logHost server
#if names are the same, cis has passed
class cis_3_3:
    def __init__(self , logDirKey , syslogServer = str):
        self.cis_3_3_passed = False
        if logDirKey.value == syslogServer:
            self.cis_3_3_passed = True
    def __str__(self):
        return str(self.cis_3_3_passed)

#input:
#logDirKey: a vim.option.OptionValue managed object
#if parsed value parameters equal cis, then cis has passed
class cis_4_2:
    def __init__(self, logDirKey):
        self.cis_4_2_passed = False
        valueString = logDirKey.value
        if 'retry=' in valueString:
            retryIndex = valueString.index('retry=')
            retryIndexLength = len('retry=')
            retryTimesPosition = retryIndex + retryIndexLength
            if int(valueString[retryTimesPosition]) < 5:
                if 'min=' in valueString:
                    minIndex = valueString.index('min=')
                    minIndexLength = len('min=')
                    minPosition = minIndex + minIndexLength
                    minN0Value = ''
                    minN1Value = ''
                    minN2Value = ''
                    minN3Value = ''
                    minN4Value = ''
                    commaCounter = 0
                    while (minPosition < len(valueString)):
                        if(valueString[minPosition] == ','):
                            commaCounter = commaCounter + 1
                            minPosition = minPosition + 1
                        if(commaCounter < 1):
                            minN0Value = minN0Value + valueString[minPosition]
                        elif(commaCounter < 2):
                            minN1Value = minN1Value + valueString[minPosition]
                        elif(commaCounter < 3):
                            minN2Value = minN2Value + valueString[minPosition]
                        elif(commaCounter < 4):
                            minN3Value = minN3Value + valueString[minPosition]
                        else:
                            minN4Value = minN4Value + valueString[minPosition]
                        minPosition = minPosition + 1

                    if minN0Value == 'disabled' and minN1Value == 'disabled' and minN2Value == 'disabled'\
                            and minN3Value == 'disabled' and minN4Value != 'disabled' and int(minN4Value) >= 14:
                        self.cis_4_2_passed = True
    def __str__(self):
        return str(self.cis_4_2_passed)