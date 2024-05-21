// Definir pines para cada segmento del display de 7 segmentos
const int a = 7;
const int b = 8;
const int c = 6;
const int d = 4;
const int e = 5;
const int f = 3;
const int g = 2;
const int buttonPin = A0; // Pin del botón

// Matriz de patrones de números de 5 a 0 para un display de ánodo común
const byte numeros[6][7] = {
  {0, 0, 0, 0, 0, 0, 0}, // 0
  {0, 1, 1, 0, 0, 0, 0}, // 1
  {1, 1, 0, 1, 1, 0, 1}, // 2
  {1, 1, 1, 1, 0, 0, 1}, // 3
  {0, 1, 1, 0, 0, 1, 1}, // 4
  {1, 0, 1, 1, 0, 1, 1}  // 5
};

// Definir los pines en un array para un fácil acceso
const int segmentos[] = {a, b, c, d, e, f, g};

void setup() {
  // Configurar los pines de los segmentos como salida
  for (int i = 0; i < 7; i++) {
    pinMode(segmentos[i], OUTPUT);
    digitalWrite(segmentos[i], HIGH); // Apagar todos los segmentos al inicio (ánodo común)
  }

  // Configurar el pin del botón como entrada
  pinMode(buttonPin, INPUT);
}

void loop() {
  static bool buttonPressed = false;
  static bool counting = false;

  // Leer el estado del botón
  int buttonState = digitalRead(buttonPin);

  // Detectar cuando se presiona el botón
  if (buttonState == HIGH && !buttonPressed && !counting) {
    buttonPressed = true;
    counting = true;

    // Realizar el conteo de 5 a 0
    for (int i = 5; i >= 0; i--) {
      mostrarNumero(i);
      delay(1000); // Esperar un segundo antes de mostrar el siguiente número
    }

    counting = false;
    apagarDisplay(); // Apagar el display después del conteo
  }

  // Detectar cuando se libera el botón
  if (buttonState == LOW && buttonPressed) {
    buttonPressed = false;
  }
}

// Función para mostrar un número en el display
void mostrarNumero(int numero) {
  // Encender los segmentos correspondientes al número
  for (int i = 0; i < 7; i++) {
    digitalWrite(segmentos[i], numeros[numero][i] ? LOW : HIGH); // Ánodo común
  }
}

// Función para apagar el display
void apagarDisplay() {
  for (int i = 0; i < 7; i++) {
    digitalWrite(segmentos[i], HIGH); // Apagar todos los segmentos (ánodo común)
  }
}
