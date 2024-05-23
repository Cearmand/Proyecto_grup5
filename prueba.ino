#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Definir los pines conectados a los segmentos del display de 7 segmentos
const int segmentos[7] = {2, 3, 4, 5, 6, 7, 8}; // A, B, C, D, E, F, G

// Mapeo de dígitos en el display de 7 segmentos (0-9) para cátodo común
const byte digitos[10] = {
  B0111111,  // 0
  B0000110,  // 1
  B1011011,  // 2
  B1001111,  // 3
  B1100110,  // 4
  B1101101,  // 5
  B1111101,  // 6
  B0000111,  // 7
  B1111111,  // 8
  B1101111   // 9
};

const int botonPin = 9; // Pin conectado al botón
const int potenciometroPin = A3; // Pin conectado al potenciómetro
const int ledPin = 10; // Pin conectado al LED

// Inicializar el LCD con la dirección I2C 0x27
LiquidCrystal_I2C lcd(0x27, 16, 2);

bool botonActivado = false; // Variable para controlar el estado del botón

void setup() {
  // Inicializar el LCD
  lcd.init();
  lcd.backlight();

  // Configurar los pines de los segmentos como salidas
  for (int i = 0; i < 7; i++) {
    pinMode(segmentos[i], OUTPUT);
    digitalWrite(segmentos[i], HIGH); // Apagar todos los segmentos al inicio (cátodo común)
  }
  
  pinMode(botonPin, INPUT_PULLUP); // Configurar el pin del botón como entrada con resistencia pull-up interna
  pinMode(ledPin, OUTPUT); // Configurar el pin del LED como salida

  Serial.begin(9600); // Iniciar comunicación serial
}

void loop() {
  // Leer el valor del potenciómetro y enviarlo por el puerto serie
  int valorPotenciometro = analogRead(potenciometroPin);
  Serial.println(valorPotenciometro);
  delay(100); // Pequeña pausa

  // Esperar a que se presione el botón físico
  if (digitalRead(botonPin) == LOW) {
    // Mandar mensaje al monitor serial indicando que el botón ha sido presionado
    Serial.println("Boton presionado");
    // Activar el botón
    botonActivado = true;
  }

  // Si el botón está activado, realizar la secuencia
  if (botonActivado) {
    // Borrar el LCD
    lcd.clear();

    // Realizar la cuenta regresiva
    for (int i = 5; i >= 0; i--) { // Contador regresivo de 5 a 0
      // Mostrar el número en el display de 7 segmentos
      mostrarNumero(i);

      // Mostrar mensajes alternativos en el LCD
      if (i > 2) {
        lcd.setCursor(0, 0);
        lcd.print("Preparate Para");
        lcd.setCursor(0, 1);
        lcd.print("La Foto");
      } else {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("SONRIAN!");
      }

      // Si el contador llega a 0, encender el LED durante un segundo
      if (i == 0) {
        digitalWrite(ledPin, HIGH); // Encender el LED conectado al pin 10
        delay(3000); // Esperar un segundo
        digitalWrite(ledPin, LOW); // Apagar el LED
      }

      delay(1000); // Esperar un segundo antes de actualizar el display
    }

    // Borrar el LCD después de la cuenta regresiva
    lcd.clear();

    // Mostrar "Imagen guardada" en el LCD
    lcd.setCursor(0, 0);
    lcd.print("Guardando imagen");
    delay(3000);
    lcd.clear();
    lcd.print(".");
    delay(1000);
    lcd.clear();
    lcd.print("..");
    delay(1000);
    lcd.clear();
    lcd.print("...");
    delay(2000);
    lcd.clear();
    lcd.setCursor(0, 1);
    lcd.print("Imagen guardada");

    // Reiniciar el estado del botón
    botonActivado = false;

    // Esperar a que se suelte el botón físico
    while (digitalRead(botonPin) == LOW) {
      delay(10); // Pequeña pausa
    }
  }
}

void mostrarNumero(int num) {
  // Mostrar el número en el display de 7 segmentos (cátodo común)
  for (int i = 0; i < 7; i++) {
    digitalWrite(segmentos[i], bitRead(digitos[num], i) == 1 ? HIGH : LOW);
  }
}