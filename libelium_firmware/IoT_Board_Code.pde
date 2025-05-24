
// Library include
#include <WaspSensorGas_v30.h>
#include <WaspFrame.h>
#include <WaspLoRaWAN.h>
#include <WaspSensorGas_Pro.h>

// socket to use
//////////////////////////////////////////////
uint8_t socket = SOCKET0;
//////////////////////////////////////////////

// Device parameters for Back-End registration
////////////////////////////////////////////////////////////
char DEVICE_EUI[]  = "70B3D57ED006681D";
char APP_EUI[] = "0000000000000000";
char APP_KEY[] = "3622B6702172BB30FF5872B3C8C3F4B5"; 
////////////////////////////////////////////////////////////

// Define port to use in Back-End: from 1 to 223
uint8_t PORT = 1;

// variable
uint8_t error;
uint8_t error_config = 0;

//sensors start
// O2 Sensor must be connected in SOCKET_1
O2SensorClass O2Sensor(SOCKET_1);
// CO Sensor must be connected physically in SOCKET_4
COSensorClass COSensor;
// NO2 Sensor must be connected physically in SOCKET_3
NO2SensorClass NO2Sensor;

// Percentage values of Oxygen
#define POINT1_PERCENTAGE 0.0
#define POINT2_PERCENTAGE 5.0

// Calibration Voltage Obtained during calibration process (in mV)
#define POINT1_VOLTAGE 0.35
#define POINT2_VOLTAGE 2.0

// Concentratios used in calibration process CO
#define POINT1_PPM_CO 100.0   // <--- Ro value at this concentration
#define POINT2_PPM_CO 300.0   // 
#define POINT3_PPM_CO 1000.0  // 

// Calibration resistances obtained during calibration process CO
#define POINT1_RES_CO 230.30 // <-- Ro Resistance at 100 ppm. Necessary value.
#define POINT2_RES_CO 40.665 //
#define POINT3_RES_CO 20.300 //

// Concentrations used in calibration process
#define POINT1_PPM_NO2 10.0   // <-- Normal concentration in air
#define POINT2_PPM_NO2 50.0
#define POINT3_PPM_NO2 100.0

// Calibration voltages obtained during calibration process (in KOHMs)
#define POINT1_RES_NO2 45.25  // <-- Rs at normal concentration in air
#define POINT2_RES_NO2 25.50
#define POINT3_RES_NO2 3.55

//O2
float concentrations[] = {POINT1_PERCENTAGE, POINT2_PERCENTAGE};
float voltages[] =       {POINT1_VOLTAGE, POINT2_VOLTAGE};

// Define the number of calibration points CO
#define numPoints 3
//co
float concentrationsCO[] = { POINT1_PPM_CO, POINT2_PPM_CO, POINT3_PPM_CO };
float resValuesCO[] =      { POINT1_RES_CO, POINT2_RES_CO, POINT3_RES_CO };
//no2
float concentrationsNO2[] = {POINT1_PPM_NO2, POINT2_PPM_NO2, POINT3_PPM_NO2};
float voltagesNO2[] =       {POINT1_RES_NO2, POINT2_RES_NO2, POINT3_RES_NO2};

char node_ID[] = "Sensor_gas_reading";

void setup()
{

  USB.ON();
  USB.println(F("Sensor reading..."));

  //sensor setup start
  O2Sensor.setCalibrationPoints(voltages, concentrations);
  // Calculate the slope and the intersection of the logarithmic function
  COSensor.setCalibrationPoints(resValuesCO, concentrationsCO, numPoints);
  // Calculate the slope and the intersection of the logarithmic function
  NO2Sensor.setCalibrationPoints(voltagesNO2, concentrationsNO2, numPoints);

  ///////////////////////////////////////////
  // 1. Turn on the board
  ///////////////////////////////////////////

  // Switch ON and configure the Gases Board
  Gases.ON();
  // Switch ON the SOCKET_1
  O2Sensor.ON();
  // Switch ON the sensor socket
  COSensor.ON();
  // Switch ON the sensor socket
  NO2Sensor.ON();
  //sensor setup end

  USB.println(F("------------------------------------"));
  USB.println(F("Module configuration"));
  USB.println(F("------------------------------------\n"));


  //////////////////////////////////////////////
  // 1. Switch on
  //////////////////////////////////////////////

  error = LoRaWAN.ON(socket);

  // Check status
  if ( error == 0 )
  {
    USB.println(F("1. Switch ON OK"));
  }
  else
  {
    USB.print(F("1. Switch ON error = "));
    USB.println(error, DEC);
    error_config = 1;
  }


  //////////////////////////////////////////////
  // 2. Change data rate
  //////////////////////////////////////////////

  error = LoRaWAN.setDataRate(3);

  // Check status
  if ( error == 0 )
  {
    USB.println(F("2. Data rate set OK"));
  }
  else
  {
    USB.print(F("2. Data rate set error= "));
    USB.println(error, DEC);
    error_config = 2;
  }


  //////////////////////////////////////////////
  // 3. Set Device EUI
  //////////////////////////////////////////////

  error = LoRaWAN.setDeviceEUI(DEVICE_EUI);

  // Check status
  if ( error == 0 )
  {
    USB.println(F("3. Device EUI set OK"));
  }
  else
  {
    USB.print(F("3. Device EUI set error = "));
    USB.println(error, DEC);
    error_config = 3;
  }

  //////////////////////////////////////////////
  // 4. Set Application EUI
  //////////////////////////////////////////////

  error = LoRaWAN.setAppEUI(APP_EUI);

  // Check status
  if ( error == 0 )
  {
    USB.println(F("4. Application EUI set OK"));
  }
  else
  {
    USB.print(F("4. Application EUI set error = "));
    USB.println(error, DEC);
    error_config = 4;
  }

  //////////////////////////////////////////////
  // 5. Set Application Session Key
  //////////////////////////////////////////////

  error = LoRaWAN.setAppKey(APP_KEY);

  // Check status
  if ( error == 0 )
  {
    USB.println(F("5. Application Key set OK"));
  }
  else
  {
    USB.print(F("5. Application Key set error = "));
    USB.println(error, DEC);
    error_config = 5;
  }

  /////////////////////////////////////////////////
  // 6. Join OTAA to negotiate keys with the server
  /////////////////////////////////////////////////

  error = LoRaWAN.joinOTAA();

  // Check status
  if ( error == 0 )
  {
    USB.println(F("6. Join network OK"));
  }
  else
  {
    USB.print(F("6. Join network error = "));
    USB.println(error, DEC);
    error_config = 6;
  }


  //////////////////////////////////////////////
  // 7. Save configuration
  //////////////////////////////////////////////

  error = LoRaWAN.saveConfig();

  // Check status
  if ( error == 0 )
  {
    USB.println(F("7. Save configuration OK"));
  }
  else
  {
    USB.print(F("7. Save configuration error = "));
    USB.println(error, DEC);
    error_config = 7;
  }

  //////////////////////////////////////////////
  // 8. Switch off
  //////////////////////////////////////////////

  error = LoRaWAN.OFF(socket);

  // Check status
  if ( error == 0 )
  {
    USB.println(F("8. Switch OFF OK"));
  }
  else
  {
    USB.print(F("8. Switch OFF error = "));
    USB.println(error, DEC);
    error_config = 8;
  }

  if (error_config == 0) {
    USB.println(F("\n---------------------------------------------------------------"));
    USB.println(F("Module configured"));
    USB.println(F("After joining through OTAA, the module and the network exchanged "));
    USB.println(F("the Network Session Key and the Application Session Key which "));
    USB.println(F("are needed to perform communications. After that, 'ABP mode' is used"));
    USB.println(F("to join the network and send messages after powering on the module"));
    USB.println(F("---------------------------------------------------------------\n"));
    USB.println();
  }
  else {
    USB.println(F("\n---------------------------------------------------------------"));
    USB.println(F("Module not configured"));
    USB.println(F("Check OTTA parameters and reestart the code."));
    USB.println(F("If you continue executing the code, frames will not be sent."));
    USB.println(F("\n---------------------------------------------------------------"));
  }

}




void loop()
{
  //sensor loop start
  // O2 Sensor does not need power suplly
  float O2Vol = O2Sensor.readVoltage();

  float COVol = COSensor.readVoltage();          // Voltage value of the sensor
  float CORes = COSensor.readResistance();       // Resistance of the sensor
  float COPPM = COSensor.readConcentration(); // PPM value of CO

  // PPM value of NO2
  float NO2Vol = NO2Sensor.readVoltage();       // Voltage value of the sensor
  float NO2Res = NO2Sensor.readResistance();    // Resistance of the sensor
  float NO2PPM = NO2Sensor.readConcentration(); // PPM value of NO2



  USB.print(F("O2 concentration Estimated: "));
  USB.print(O2Vol);
  USB.print(F(" mV | "));
  
  delay(100);

  // Read the concentration value in %
  float O2Val = O2Sensor.readConcentration();


  USB.print(F(" O2 concentration Estimated: "));
  USB.print(O2Val);
  USB.println(F(" %"));

  // Print of the results
  USB.print(F("CO Sensor Voltage: "));
  USB.print(COVol);
  USB.print(F(" mV |"));

  // Print of the results
  USB.print(F(" CO Sensor Resistance: "));
  USB.print(CORes);
  USB.print(F(" Ohms |"));

  USB.print(F(" CO concentration Estimated: "));
  USB.print(COPPM);
  USB.println(F(" ppm"));

  // Print of the results
  USB.print(F("NO2 Sensor Voltage: "));
  USB.print(NO2Vol);
  USB.print(F(" V |"));

  // Print of the results
  USB.print(F(" NO2 Sensor Resistance: "));
  USB.print(NO2Res);
  USB.print(F(" Ohms |"));
  
  delay(100);
   // read Humidity sensor connected to ANALOG7
   
  int humidity = Utils.readHumidity();
  // Print of the results
  USB.print(F(" Humidity: "));
  USB.print(humidity);
  //////////////////////////////////////////////
  // 1. Switch on
  //////////////////////////////////////////////

  error = LoRaWAN.ON(socket);

  // Check status
  if ( error == 0 )
  {
    USB.println(F("1. Switch ON OK"));
  }
  else
  {
    USB.print(F("1. Switch ON error = "));
    USB.println(error, DEC);
  }


  //////////////////////////////////////////////
  // 2. Join network
  //////////////////////////////////////////////

  error = LoRaWAN.joinABP();

  // Check status
  if ( error == 0 )
  {
    USB.println(F("2. Join network OK"));

    //////////////////////////////////////////////


  
    // Multiply by 100 to preserve up to two decimal places and cast it to uint32_t
    uint32_t sendO2Int = static_cast<uint32_t>(O2Val * 100.0);
    uint32_t sendCOInt = static_cast<uint32_t>(COPPM * 100.0);
    uint32_t sendNO2Int = static_cast<uint32_t>(NO2PPM * 100.0);
    uint32_t sendHumidityInt = static_cast<uint32_t>(humidity * 100.0);
    USB.println(F("\nsendO2Int: "));
    USB.print((sendO2Int));
    USB.println(F("\nsendCOInt: "));
    USB.print((sendCOInt));
    USB.println(F("\nsendNO2Int: "));
    USB.print((sendNO2Int));
    USB.println(F("\n"));
   USB.println(F("\n sendHumidityInt: "));
   USB.print((sendHumidityInt));

  
    byte data[16]; // the data we shall sent to the cloud. It can only 8 bits per cell

    // Store the unsigned 32 bit integer values in the byte array
    // How it works, it shift the value by multiples of 8 in order to isolate the byte we want
    //Then, the result is bitwise AND with 0xFF ensures that only the lowest 8 bits are retained
    //The resulting value is stored in data 
    data[0] = (sendO2Int >> 24) & 0xFF;//The bits being shifted and stored are the 8 most significant bits, ranging from bit 31 to bit 24.
    data[1] = (sendO2Int >> 16) & 0xFF;//The bits being shifted and stored are the next 8 bits, ranging from bit 23 to bit 16.
    data[2] = (sendO2Int >> 8) & 0xFF;//The bits being shifted and stored are the next 8 bits, ranging from bit 15 to bit 8.
    data[3] = sendO2Int & 0xFF;//The bits being stored directly are the 8 least significant bits, ranging from bit 7 to bit 0.

    data[4] = (sendCOInt >> 24) & 0xFF;//The bits being shifted and stored are the 8 most significant bits, ranging from bit 31 to bit 24.
    data[5] = (sendCOInt >> 16) & 0xFF;//The bits being shifted and stored are the next 8 bits, ranging from bit 23 to bit 16.
    data[6] = (sendCOInt >> 8) & 0xFF;//The bits being shifted and stored are the next 8 bits, ranging from bit 15 to bit 8.
    data[7] = sendCOInt & 0xFF;//The bits being stored directly are the 8 least significant bits, ranging from bit 7 to bit 0.

    data[8] = (sendNO2Int >> 24) & 0xFF;//The bits being shifted and stored are the 8 most significant bits, ranging from bit 31 to bit 24.
    data[9] = (sendNO2Int >> 16) & 0xFF;//The bits being shifted and stored are the next 8 bits, ranging from bit 23 to bit 16.
    data[10] = (sendNO2Int >> 8) & 0xFF;//The bits being shifted and stored are the next 8 bits, ranging from bit 15 to bit 8.
    data[11] = sendNO2Int & 0xFF;//The bits being stored directly are the 8 least significant bits, ranging from bit 7 to bit 0.

    data[12] = (sendHumidityInt >> 24) & 0xFF;//The bits being shifted and stored are the 8 most significant bits, ranging from bit 31 to bit 24.
    data[13] = (sendHumidityInt >> 16) & 0xFF;//The bits being shifted and stored are the next 8 bits, ranging from bit 23 to bit 16.
    data[14] = (sendHumidityInt >> 8) & 0xFF;//The bits being shifted and stored are the next 8 bits, ranging from bit 15 to bit 8.
    data[15] = sendHumidityInt & 0xFF;//The bits being stored directly are the 8 least significant bits, ranging from bit 7 to bit 0.

    error = LoRaWAN.sendConfirmed(PORT, data, 16);//sends data to the things network


    // Error messages:
    /*
       '6' : Module hasn't joined a network
       '5' : Sending error
       '4' : Error with data length
       '2' : Module didn't response
       '1' : Module communication error
    */
    // Check status
    if ( error == 0 )
    {
      USB.println(F("3. Send Confirmed packet OK"));
      if (LoRaWAN._dataReceived == true)
      {
        USB.print(F("   There's data on port number "));
        USB.print(LoRaWAN._port, DEC);
        USB.print(F(".\r\n   Data: "));
        USB.println(LoRaWAN._data);
      }
    }
    else
    {
      USB.print(F("3. Send Confirmed packet error = "));
      USB.println(error, DEC);
    }
  }
  else
  {
    USB.print(F("2. Join network error = "));
    USB.println(error, DEC);
  }


  //////////////////////////////////////////////
  // 4. Switch off
  //////////////////////////////////////////////

  error = LoRaWAN.OFF(socket);

  // Check status
  if ( error == 0 )
  {
    USB.println(F("4. Switch OFF OK"));
  }
  else
  {
    USB.print(F("4. Switch OFF error = "));
    USB.println(error, DEC);
    USB.println();
  }
  delay(3000);
}

