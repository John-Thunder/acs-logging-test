""" 
A basic CLI for examining the logs and their analysis.
"""

import config
import notify
from log import Log
from messageQueue import Queue
from summaryTable import SummaryTable

import json
import optparse
import pickle

def printSummary():
  log = Log()
  log.debug("Displaying summary for queue called '" + config.AZURE_STORAGE_QUEUE_NAME + "' and table called '" + config.AZURE_STORAGE_SUMMARY_TABLE_NAME + "' in storage account called '" + config.AZURE_STORAGE_ACCOUNT_NAME + "'")

  table_service = getTableService() 
  queue_service = getQueueService()

  summary = "Queue Length is approximately: " + str(queue_service.getLength()) + "\n"
  summary = summary + "Processing of last event took: " + str(table_service.getLastProcessingTime()) + "ms\n\n"
  summary = summary + "Processed events:\n"
  summary = summary + "Errors: " + str(table_service.getCount("ERROR")) + "\n"
  summary = summary + "Warnings: " + str(table_service.getCount("WARNING")) + "\n"
  summary = summary + "Infos: " + str(table_service.getCount("INFO")) + "\n"
  summary = summary + "Debugs: " + str(table_service.getCount("DEBUG")) + "\n"
  summary = summary + "Correct: " + str(table_service.getCount("CORRECT")) + "\n"
  summary = summary + "Incorrect: " + str(table_service.getCount("INCORRECT")) + "\n"
  summary = summary + "Others: " + str(table_service.getCount("OTHER")) + "\n"
  print(summary)
  notify.info(summary)

def getQueueService():
  queue_service = Queue(account_name = config.AZURE_STORAGE_ACCOUNT_NAME, account_key=config.AZURE_STORAGE_ACCOUNT_KEY, queue_name=config.AZURE_STORAGE_QUEUE_NAME)
  return queue_service

def getTableService():
  return SummaryTable(config.AZURE_STORAGE_ACCOUNT_NAME, config.AZURE_STORAGE_ACCOUNT_KEY, config.AZURE_STORAGE_SUMMARY_TABLE_NAME)

def dumpUnprocessedLogs():
  print ("Unproccessed logs")
  try:
      with open(config.UNPROCESSED_LOG_FILE, 'r') as f:
          log = f.read()
      print (log)
  except:
      print("No logs waiting to be processed")

def dumpLogs():
  print ("Proccessed logs")
  try:
      with open(config.PROCESSED_LOG_FILE, 'r') as f:
          log = f.read()
      print (log)
  except:
      print("No logs have been processed")

def readSummary():
  try:
    with open(config.SUMMARY_LOG_FILE, 'r') as f:
      summary = json.loads(f.read())
  except FileNotFoundError:
    summary = {'ERRORS': 0, 'WARNINGS':0, 'INFOS':0}
  return summary

def deleteQueue():
  log = Log()
  getQueueService().delete_queue(config.AZURE_STORAGE_QUEUE_NAME)
  log.info("Queue deleted: " + config.AZURE_STORAGE_QUEUE_NAME)

def createQueue():
  log = Log()
  log.debug("Creating queue named: " + config.AZURE_STORAGE_QUEUE_NAME)
  queue_service = getQueueService()

def createTable():
  log.debug("Creating table named: " + config.AZURE_STORAGE_SUMMARY_TABLE_NAME)
  table = SummaryTable(config.AZURE_STORAGE_ACCOUNT_NAME, config.AZURE_STORAGE_ACCOUNT_KEY, config.AZURE_STORAGE_SUMMARY_TABLE_NAME)

def deleteTable():
  log = Log()
  getTableService().deleteTable(config.AZURE_STORAGE_SUMMARY_TABLE_NAME)
  log.info("Table deleted: " + config.AZURE_STORAGE_SUMMARY_TABLE_NAME)
  
if __name__ == "__main__":
  log = Log()

  usage = "usage: %prog [options] command\n\n"
  usage += "summary\t\t- print approximate queue length and current analysis\n"
  usage += "length\t\t- print approximate queue length\n"
  usage += "createQueue\t- create the queue\n"
  usage += "deleteQueue\t- delete the current queue\n"
  usage += "createTable\t- create the table\n"
  usage += "deleteTable\t- delete the table\n"
  usage += "config\t\t- display the current configuration"

  p = optparse.OptionParser(usage=usage)
  options, arguments = p.parse_args()

  cmd = arguments[0]
  
  if cmd == "config":
    help(config)
    exit()

  if cmd == "summary":
    printSummary()
  elif cmd == "length":
    print(str(getQueueService().getLength()))
  elif cmd == "deleteQueue":
    deleteQueue()
  elif cmd == "createQueue":
    createQueue()
  elif cmd == "deleteTable":
    deleteTable()
  elif cmd == "createTable":
    createTable()
  else:
    log.error("Unkown command: " + cmd)
    print(usage)
