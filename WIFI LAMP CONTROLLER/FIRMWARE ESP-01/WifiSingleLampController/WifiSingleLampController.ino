/*
 *  This sketch demonstrates how to set up a simple HTTP-like server.
 *  The server will set a GPIO pin depending on the request
 *    http://server_ip/gpio/0 will set the GPIO2 low,
 *    http://server_ip/gpio/1 will set the GPIO2 high
 *  server_ip is the IP address of the ESP8266 module, will be 
 *  printed to Serial when the module is connected.
 */

#include <ESP8266WiFi.h>

const char* ssid = "ssid";
const char* password = "pass";
IPAddress ip(192, 168, 43, 30);
IPAddress gateway(192, 168, 1, 1); // set gateway to match your network
IPAddress subnet(255, 255, 255, 0); // set subnet mask to match your

// Create an instance of the server
// specify the port to listen on as an argument
WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  delay(10);

// prepare GPIO
  pinMode(2, OUTPUT);
  digitalWrite(2, 0);
  
//Disconnect WiFi
  WiFi.disconnect();
  WiFi.softAPdisconnect();
  WiFi.mode(WIFI_OFF);
  delay(500);

//Set WiFi in static IP mode
  WiFi.mode(WIFI_STA);
  WiFi.config(ip,gateway,subnet);

//Connect to AP
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
  Serial.println(WiFi.localIP());
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
  String req = client.readStringUntil('\r');
  Serial.println(req);
  client.flush();
  
// Match the request and set GPIO
  if (req.indexOf("/LED0") != -1) digitalWrite(2, LOW);
  if (req.indexOf("/LED1") != -1) digitalWrite(2, HIGH);
  
  client.flush();

  // Prepare the response
  String s = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE HTML>\r\n<html>\r\n";
  s += "<h1><a href='/LED0'>Switch off LED</a></h1>";
  s += "<h1><a href='/LED1'>Switch on LED</a></h1>";
  s += "</html>\n";

  // Send the response to the client
  client.print(s);
  delay(1);
  Serial.println("Client disonnected");

  // The client will actually be disconnected 
  // when the function returns and 'client' object is detroyed
}

