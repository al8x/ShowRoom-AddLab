#include <ESP8266WiFi.h>
#include <Servo.h>

const char* ssid = "ssid";//type your ssid
const char* password = "pass";//type your password

int servoPos = 45;
int LED = 0;

int ledPin = 4; // GPIO2 of ESP8266
WiFiServer server(80);
Servo myservo;

void setup() {
  Serial.begin(115200);
  delay(10);
  myservo.attach(16);
 
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
   
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
   
  WiFi.begin(ssid, password);
   
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
   
  // Start the server
  server.begin();
  Serial.println("Server started");
 
  // Print the IP address
  Serial.print("Use this URL to connect: ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");

  myservo.write(0);
  delay(500);
  myservo.write(45);
 

}
 
void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
   
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){
    delay(1);
  }
   
  // Read the first line of the request
  String request = client.readStringUntil('\r');
  char requete[10];
  request.toCharArray(requete,10);
  Serial.println(request);
  client.flush();
   
  // Match the request

  if (requete[5] == 'L')
  {
    if (requete[6] == 'E')
    {
      if (requete[7] == 'D')
      {
        if (requete[8] == '0')
        {
          digitalWrite(ledPin,LOW);
        }
        if (requete[8] == '1')
        {
          digitalWrite(ledPin,HIGH);
        }
      }
    }
  }

  
 
// Set ledPin according to the request
//digitalWrite(ledPin, value);
   
 
  // Return the response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); //  do not forget this one
  client.println("<!DOCTYPE HTML>");
  client.println("<meta http-equiv='refresh' content='5; URL=/refresh'>");
  client.println("<html>");

  client.println("<H1>Serre automatique</H1>");
  client.println("<H2><a href=\"/ARROSAGE=1\">ARROSAGE ON</a> </H2>");
  client.println("<H2><a href=\"/ARROSAGE=0\">ARROSAGE OFF</a> </H2><br>");

  client.println("<H2><a href=\"/LED1\">LED ON</a> </H2>");
  client.println("<H2><a href=\"/LED0\">LED OFF</a> </H2><br>");
/*
  if(value == HIGH) {
    client.print("On");  
    client.println("<br><br>");
    client.println("Click <a href=\"/LED=OFF\">here</a> turn the LED on pin 4 OFF<br>");
  } else {
    client.print("Off");
    client.println("<br><br>");
    client.println("Click <a href=\"/LED=ON\">here</a> turn the LED on pin 4 ON<br>");
  }
  */
  client.println("</html>");
 
  delay(1);
  Serial.println("Client disonnected");
  Serial.println("");
 
}

