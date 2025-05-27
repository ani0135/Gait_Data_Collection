#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>

#define ADS1115_ADDRESS 0x48  // I2C address of the ADS1115

// Configuration register addresses
#define ADS1115_REG_CONVERSION 0x00
#define ADS1115_REG_CONFIG 0x01

// Configuration register bits for faster sampling
#define ADS1115_CONFIG_OS_SINGLE 0x8000  // Start a single conversion
#define ADS1115_CONFIG_PGA_1 0x0000  // Gain setting: ±4.096V
#define ADS1115_CONFIG_MODE_SINGLE 0x0100  // Single-shot mode
#define ADS1115_CONFIG_DR_3300SPS 0x00E0  // Data rate: 3,300 SPS

// MUX selection for different channels
#define ADS1115_CONFIG_MUX_SINGLE_0 0x4000  // Single-ended mode (channel 0)
#define ADS1115_CONFIG_MUX_SINGLE_1 0x5000  // Single-ended mode (channel 1)
#define ADS1115_CONFIG_MUX_SINGLE_2 0x6000  // Single-ended mode (channel 2)

// WiFi Credentials
// const char* ssid = "IIT-Mandi-WiFi";    // Wi-Fi SSID
// const char* password = "wifi@iit"; // Wi-Fi Password

// // UDP server information (ROS 2 system)
// const char* serverIP = "172.16.6.57"; // ROS 2 System's IP
const char* ssid = "Nigam";    // Wi-Fi SSID
const char* password = "P@$$word"; // Wi-Fi Password

// UDP server information (ROS 2 system)
const char* serverIP = "192.168.1.107"; // ROS 2 System's IP
const int serverPort = 5005;            // Port on ROS 2 system

// UDP Settings
WiFiUDP udp;

// Variables to count data
unsigned long lastMillis = 0;
unsigned int packetCount = 0;

// Function to read values from ADS1115
String FlexiForceReading() {
  // Read channel 0 (Heel Outer or Heel2)
  writeRegister(ADS1115_REG_CONFIG, ADS1115_CONFIG_OS_SINGLE | ADS1115_CONFIG_MUX_SINGLE_0 | ADS1115_CONFIG_PGA_1 | ADS1115_CONFIG_MODE_SINGLE | ADS1115_CONFIG_DR_3300SPS);
  delay(1);  // Small delay to wait for the conversion to complete
  int16_t reading1 = readRegister(ADS1115_REG_CONVERSION);

  // Read channel 1 (Heel Inner or Heel1)
  writeRegister(ADS1115_REG_CONFIG, ADS1115_CONFIG_OS_SINGLE | ADS1115_CONFIG_MUX_SINGLE_1 | ADS1115_CONFIG_PGA_1 | ADS1115_CONFIG_MODE_SINGLE | ADS1115_CONFIG_DR_3300SPS);
  delay(1);  // Small delay to wait for the conversion to complete
  int16_t reading2 = readRegister(ADS1115_REG_CONVERSION);

  // Read channel 2 (Toe)
  writeRegister(ADS1115_REG_CONFIG, ADS1115_CONFIG_OS_SINGLE | ADS1115_CONFIG_MUX_SINGLE_2 | ADS1115_CONFIG_PGA_1 | ADS1115_CONFIG_MODE_SINGLE | ADS1115_CONFIG_DR_3300SPS);
  delay(1);  // Small delay to wait for the conversion to complete
  int16_t reading3 = readRegister(ADS1115_REG_CONVERSION);

  // Prepare the readings as a string
  String readings = String(reading3) + " " + 
                    String(reading2) + " " + 
                    String(reading1);
  return readings;
}

void setup() {
  // Initialize Serial for debugging
  Serial.begin(9600);

  // Initialize I2C communication
  Wire.begin();

  // Initialize WiFi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }
  Serial.println("Connected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Initialize UDP
  udp.begin(12345);
  Serial.println("UDP started");

  Serial.println("ADS1115 initialized");
}

void loop() {
  // Get readings
  String readingsFlexi = FlexiForceReading();

  // Create JSON data
  String data = "{\"L_Leg\": \"" + readingsFlexi + "\"}";
  // Serial.println(data);

  // Send UDP packet
  udp.beginPacket(serverIP, serverPort);
  udp.write(data.c_str(), data.length());
  udp.endPacket();

  // Increment packet count
  packetCount++;

  // Check if one second has elapsed
  unsigned long currentMillis = millis();
  if (currentMillis - lastMillis >= 1000) {
    // Print the count and reset
    Serial.print("Packets sent in last second: ");
    Serial.println(packetCount);
    packetCount = 0;
    lastMillis = currentMillis;
  }

  // No delay here to maximize packet sending rate
  // delay(100);
}

void writeRegister(uint8_t reg, uint16_t value) {
  Wire.beginTransmission(ADS1115_ADDRESS);
  Wire.write(reg);
  Wire.write(value >> 8);  // Write high byte
  Wire.write(value & 0xFF);  // Write low byte
  Wire.endTransmission();
}

int16_t readRegister(uint8_t reg) {
  Wire.beginTransmission(ADS1115_ADDRESS);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom(ADS1115_ADDRESS, 2);
  int16_t result = (Wire.read() << 8) | Wire.read();
  return result;
}
