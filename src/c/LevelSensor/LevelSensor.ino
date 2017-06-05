#include "DigitShield.h"
#include <Ethernet2.h>
//#include <EthernetServer.h>
#include <util.h>
#include <SoftwareSerial.h>

byte mac[] = { 0x90, 0xA2, 0XDA, 0X10, 0XFB, 0XFE };
//byte ip[] = { 192, 168, 1, 177 };
int dist;
unsigned long fails;

SoftwareSerial sonarSerial(8, 9); // rx: pin8, tx: pin9
EthernetServer server(80); // port 80


void setup() {
  
  fails = 0;
  dist = 0;
  
  DigitShield.begin();
  
  sonarSerial.begin(9600);
  Serial.begin(9600);
  
  delay(2000);
  
  while(true) {
    if (Ethernet.begin(mac) == 0) {
      Serial.println("Failed to establish ethernet connection");
      Serial.println("Retrying...");
      delay(1000);
    }
    else {
      break;
    }
  }
  
  Serial.print("Created server at: ");
  Serial.println(Ethernet.localIP());
}

void loop() {

  try_update_dist();
  
  DigitShield.setValue(dist);
  
  String json = "{\"distance\": {\"value\": " + String(dist) + ", \"units\": \"mm\"}, " +
                "\"last_update\": {\"value\": " + String(fails) + ", \"units\": \"s\"}}";
  
  Serial.println(json);
  
  http_respond(json);

  delay(1000);
}

void try_update_dist() 
{
  //Serial.flush();
  //delay(200);
  
  int bytes = sonarSerial.available();
  if (bytes > 5) 
  {
    
    byte buf[bytes];
    
    sonarSerial.readBytes(buf, bytes);
    Serial.write("Serial buf: ");
    Serial.write((char*)buf, bytes);
    Serial.write("\n");
    for (int i=0; i<bytes; i++)
    {
      if (buf[i] == 'R')
      {
        if ((bytes-i) >= 5) 
        {

          if (isOK(buf[i+1]) &&
              isOK(buf[i+2]) &&
              isOK(buf[i+3]) &&
              isOK(buf[i+4]) && 
              (buf[i+5] == 0x0D)) 
          {
            dist = (buf[i+1] - '0') * 1000 +
                  (buf[i+2] - '0') * 100 +
                  (buf[i+3] - '0') * 10 +
                  (buf[i+4] - '0') * 1;
            fails = 0;
            return;
          }
        }
      }
    }
    fails++;
  }
  else {
    fails++;
  }
}

bool isOK(byte val) {
  bool ok = false;
  if ((val >= '0') && (val <= '9'))  //ASCII between 0 and 9
  {
    ok = true;
  }
  return ok;
}

void http_respond(String json) {
    EthernetClient client = server.available();
  if (client) {
    Serial.println("New client");
    bool currentLineIsBlank = true;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        Serial.write(c);
        
        if (c == '\n' && currentLineIsBlank) {
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: application/json;charset=utf-8");
          client.println("Server: Arduino");
          client.println("Connection: close");
          client.println();
          client.print(json);
          client.println();
          break;
        }
        
        if (c == '\n') {
          currentLineIsBlank = true;
        }
        else if (c != '\r') {
          currentLineIsBlank = false;
        }
      }
    }
    delay(1);
    client.stop();
    Serial.println("Client disconnected");
  }
  
}

