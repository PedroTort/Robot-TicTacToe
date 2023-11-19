#include <Servo.h>

Servo myservo;
int posMaxCaneta = 55;
int posCanetaMedia = 25;
int posCaneta = 0;
int incomingByte = 0;

int posCima = 0;
int posDireita = 0;

#define EN 8

//Direction pin
#define X_DIR 5
#define Y_DIR 6

//Step pin
#define X_STP 2
#define Y_STP 3

//Fim de curso X
#define PIN_FIM_DE_CURSO_X 10

//Fim de curso Y
#define PIN_FIM_DE_CURSO_Y 9

//Servo motor
#define PIN_SERVO_MOTOR 11

//A498
int delayTime = 300;
int stps = 10;

void setup() {
  pinMode(X_DIR, OUTPUT);
  pinMode(X_STP, OUTPUT);
  pinMode(Y_DIR, OUTPUT);
  pinMode(Y_STP, OUTPUT);

  pinMode(EN, OUTPUT);
  digitalWrite(EN, LOW);

  myservo.attach(PIN_SERVO_MOTOR);
  myservo.write(posCaneta);

  pinMode(PIN_FIM_DE_CURSO_X, INPUT);
  pinMode(PIN_FIM_DE_CURSO_Y, INPUT);

  Serial.begin(9600);
  volta_posicao_inicial();
  Serial.print('a');
}


void loop() {
  bool comando_feito = recebeExecutaComando();
  if(comando_feito){
    Serial.print('a');
  }
}

bool recebeExecutaComando(){
  const char input = le_input();
  switch (input){
    case '2':
      vaiPosicao11();
      return true;
      break;
    case '5':
      vaiPosicao12();
      return true;
      break;
    case '8':
      vaiPosicao13();
      return true;
      break;
    case '1':
      vaiPosicao21();
      return true;
      break;
    case '4':
      vaiPosicao22();
      return true;
      break;
    case '7':
      vaiPosicao23();
      return true;
      break;
    case '0':
      vaiPosicao31();
      return true;
      break;
    case '3':
      vaiPosicao32();
      return true;
      break;
    case '6':
      vaiPosicao33();
      return true;
      break;
    case 'i':
      volta_posicao_inicial();
      return true;
      break;
    case 'v':
      desenhaVelha();
      return true;
      break;
    case 'o':
      desenhaCirculoV2();
      return true;
      break;
    case 'x':
      desenhaX();
      return true;
      break;
    case 's':
      posCaneta = posCanetaMedia;
      myservo.write(posCaneta);
  }
  return false;
}

const char le_input(){
  const int bufferSize = 64;  // Adjust the buffer size according to your needs
  while(Serial.available() == 0){}
  char incomingChar = Serial.read();
  if (incomingChar != '\n') {
    return incomingChar;
  } else {
    return ' ';
  }
}

// if digitalRead(PIN_FIM_DE_CURSO_X) != LOW) -> Fim de Curso Pressionado
// if digitalRead(PIN_FIM_DE_CURSO_Y) != LOW) -> Fim de Curso Pressionado

void volta_posicao_inicial(){
  while(digitalRead(PIN_FIM_DE_CURSO_Y) == LOW){
    esquerda(1);
    delay(0.5);
  }
  while(digitalRead(PIN_FIM_DE_CURSO_X) == LOW){
    baixo(1);
    delay(0.5);
  }
  
}

void cima(int steps) {
  digitalWrite(X_DIR, false);
  digitalWrite(Y_DIR, false);

  for (int i = 0; i < steps; i++) {
    digitalWrite(X_STP, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(Y_STP, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(X_STP, LOW);
    delayMicroseconds(delayTime);
    digitalWrite(Y_STP, LOW);
    delayMicroseconds(delayTime);
  }
}

void baixo(int steps) {
  digitalWrite(X_DIR, true);
  digitalWrite(Y_DIR, true);

  for (int i = 0; i < steps; i++) {
    digitalWrite(X_STP, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(Y_STP, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(X_STP, LOW);
    delayMicroseconds(delayTime);
    digitalWrite(Y_STP, LOW);
    delayMicroseconds(delayTime);
  }
}

void esquerda(int steps) {
  digitalWrite(X_DIR, false);
  digitalWrite(Y_DIR, true);

  for (int i = 0; i < steps; i++) {
    digitalWrite(X_STP, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(Y_STP, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(X_STP, LOW);
    delayMicroseconds(delayTime);
    digitalWrite(Y_STP, LOW);
    delayMicroseconds(delayTime);
  }
}

void direita(int steps) {
  digitalWrite(X_DIR, true);
  digitalWrite(Y_DIR, false);

  for (int i = 0; i < steps; i++) {
    digitalWrite(X_STP, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(Y_STP, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(X_STP, LOW);
    delayMicroseconds(delayTime);
    digitalWrite(Y_STP, LOW);
    delayMicroseconds(delayTime);
  }
}


void diagonalCimaDireita(int steps) {
  for (int i = 0; i < steps; i++) {
    cima(1);
    delay(1);
    direita(1);
  }
}

void diagonalBaixoEsquerda(int steps) {
  for (int i = 0; i < steps; i++) {
    baixo(1);
    delay(1);
    esquerda(1);
  }
}


void diagonalBaixoDireita(int steps) {
  for (int i = 0; i < steps; i++) {
    baixo(1);
    delay(1);
    direita(1);
  }
}

void diagonalCimaEsquerda(int steps) {
  for (int i = 0; i < steps; i++) {
    cima(1);
    delay(1);
    esquerda(1);
  }
}

void step(boolean dir, byte dirPin, byte stepperPin, int steps) {
  digitalWrite(dirPin, dir);
  for (int i = 0; i < steps; i++) {
    digitalWrite(stepperPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepperPin, LOW);
    delayMicroseconds(1000);
  }
}

void sobeCaneta() {
  if (posCaneta >= 0) {
    for (posCaneta; posCaneta < posMaxCaneta; posCaneta++) {
      //Serial.print(posCaneta);
      myservo.write(posCaneta);
    }
  }
  delay(200);
}

void desceCaneta() {
  if (posCaneta >= 0) {
    for (posCaneta; posCaneta > 0; posCaneta--) {
      //      Serial.print(posCaneta);
      myservo.write(posCaneta);
    }
  }
  delay(200);
}

//Inicio x = 0,y=0
void desenhaVelha() {

  int delay_movimento_caneta = 0;

  sobeCaneta();
  cima(950);

  desceCaneta();
  delay(delay_movimento_caneta);
  direita(900);

  sobeCaneta();
  delay(delay_movimento_caneta);
  cima(300);

  desceCaneta();
  delay(delay_movimento_caneta);
  esquerda(900);

  sobeCaneta();
  cima(300);
  direita(300);

  desceCaneta();
  delay(delay_movimento_caneta);
  baixo(900);

  sobeCaneta();
  delay(delay_movimento_caneta);
  direita(300);

  desceCaneta();
  //      /Serial.print("Descida 3: ");
  //  /Serial.print(posCaneta);
  //  /Serial.println();
  delay(delay_movimento_caneta);
  cima(900);

  sobeCaneta();

  volta_posicao_inicial();
}

void vaiPosicao11() {
  sobeCaneta();
  cima(1550);
}

void voltaPosicao11() {
  sobeCaneta();
  baixo(1550);
  delay(500);
}

void vaiPosicao12() {
  sobeCaneta();
  cima(1550);
  direita(300);
}

void voltaPosicao12() {
  sobeCaneta();
  baixo(1550);
  esquerda(300);
}

void vaiPosicao13() {
  sobeCaneta();
  cima(1550);
  direita(600);
}

void voltaPosicao13() {
  sobeCaneta();
  baixo(1550);
  esquerda(600);
}

void vaiPosicao21() {
  sobeCaneta();
  cima(1250);
}

void voltaPosicao21() {
  sobeCaneta();
  baixo(1250);
}

void vaiPosicao22() {
  sobeCaneta();
  cima(1250);
  direita(300);
}

void voltaPosicao22() {
  sobeCaneta();
  baixo(1250);
  esquerda(300);
}

void vaiPosicao23() {
  sobeCaneta();
  cima(1250);
  direita(600);
}

void voltaPosicao23() {
  sobeCaneta();
  baixo(1250);
  esquerda(600);
}

void vaiPosicao31() {
  sobeCaneta();
  cima(950);
}

void voltaPosicao31() {
  sobeCaneta();
  delay(500);
  baixo(950);
}

void vaiPosicao32() {
  sobeCaneta();
  cima(950);
  direita(300);
}

void voltaPosicao32() {
  sobeCaneta();
  baixo(950);
  esquerda(300);
}

void vaiPosicao33() {
  sobeCaneta();
  cima(950);
  direita(600);
}

void voltaPosicao33() {
  sobeCaneta();
  baixo(950);
  esquerda(600);
}

void venceuColuna1() {
  sobeCaneta();
  delay(300);
  cima(1550);
  direita(150);

  delay(300);
  desceCaneta();
  delay(300);
  baixo(900);

  sobeCaneta();
  delay(300);
  esquerda(150);
  baixo(650);
}

void venceuColuna2() {
  sobeCaneta();
  delay(300);
  cima(1550);
  direita(450);

  delay(300);
  desceCaneta();
  delay(300);
  baixo(900);

  sobeCaneta();
  delay(300);
  esquerda(450);
  delay(300);
  baixo(650);
}

void venceuColuna3() {
  sobeCaneta();
  delay(300);
  cima(1550);
  direita(750);

  delay(300);
  desceCaneta();
  delay(300);
  baixo(900);

  sobeCaneta();
  delay(300);
  esquerda(750);
  baixo(650);
}

void venceuLinha1() {
  sobeCaneta();
  delay(300);
  cima(800);
  direita(900);

  delay(300);
  desceCaneta();
  delay(300);
  esquerda(900);

  sobeCaneta();
  delay(300);
  baixo(800);
}

void venceuLinha2() {
  sobeCaneta();
  delay(300);
  cima(1100);
  direita(900);

  delay(300);
  desceCaneta();
  delay(300);
  esquerda(900);

  sobeCaneta();
  delay(300);
  baixo(1100);
}

void venceuLinha3() {
  sobeCaneta();
  delay(300);
  cima(1400);
  direita(900);

  delay(300);
  desceCaneta();
  delay(300);
  esquerda(900);

  sobeCaneta();
  delay(300);
  baixo(1400);
}

void venceuDiagonalEsquerdaCima() {
  sobeCaneta();
  delay(300);
  cima(650);
  direita(900);

  delay(300);
  desceCaneta();
  delay(300);
  diagonalCimaEsquerda(900);

  sobeCaneta();
  baixo(1600);
  delay(300);
}

void venceuDiagonalDireitaCima() {
  sobeCaneta();
  delay(300);
  cima(650);

  delay(300);
  desceCaneta();
  delay(300);
  diagonalCimaDireita(900);

  sobeCaneta();
  baixo(1600);
  esquerda(900);
  delay(300);
}


void desenhaX() {
  direita(80);  //indo para a posição inicial para desenhar o X
  baixo(80);

  desceCaneta();
  diagonalBaixoDireita(141);
  //delay(300);

  sobeCaneta();
  esquerda(141);
  //delay(300);

  desceCaneta();
  diagonalCimaDireita(141);
  //delay(300);

  sobeCaneta();
}

void desenhaO() {
  sobeCaneta();

  //primeiro quadrante
  ///  direita(300);
  cima(300);
  desceCaneta();
  delay(200);

  direita(70);
  diagonalBaixoDireita(70);
  baixo(70);
  diagonalBaixoEsquerda(70);
  esquerda(70);
  diagonalCimaEsquerda(70);
  cima(70);
  diagonalCimaDireita(70);

  sobeCaneta();
}

void moveHorizontal(int steps){
  if (steps>0){
    direita(steps);
  }
  else if(steps<0){
    esquerda(abs(steps));
  }
}

void moveVertical(int steps){
  if (steps>0){
    cima(steps);
  }
  else if(steps<0){
    baixo(abs(steps));
  }
}

void desenhaDiagonal(float delta_x, float delta_y){
  delta_x = round(delta_x);
  delta_y = round(delta_y);
  
  if(abs(delta_x)>=abs(delta_y)){
    int razao = abs(delta_x)/abs(delta_y);
    while(delta_x != 0 && delta_y != 0 ){
      int step = razao;
      while(step>0){
        moveHorizontal(delta_x/abs(delta_x));
        delta_x-=delta_x/abs(delta_x);
        step--;
      }
      moveVertical(delta_y/abs(delta_y));
      delta_y-=delta_y/abs(delta_y);
    }
    if(delta_x!=0){
      moveHorizontal(delta_x);
    }
  }
  else{
    int razao = abs(delta_y)/abs(delta_x);
    while(delta_x != 0 && delta_y != 0 ){
      int step = razao;
      while(step>0){
        moveVertical(delta_y/abs(delta_y));
        delta_y-=delta_y/abs(delta_y);
        step--;
      }
      moveHorizontal(delta_x/abs(delta_x));
      delta_x-=delta_x/abs(delta_x);
    }
    if(delta_y!=0){
      moveVertical(delta_y);
    }
  }
}

void desenhaCirculoV2(){
  int raio = 100;
  int delay_time = 50;
  int angle_step = 5;
  int delay_circulo = 10;

  direita(50 + 2*raio);  //indo para a posição inicial para desenhar o X
  baixo(50+raio);

  desceCaneta();

  int angulo = 0;
  float x = raio * cos(angulo * M_PI / 180);
  float y = raio * sin(angulo * M_PI / 180);
  float x_atual, delta_x;
  float y_atual, delta_y;

  while (angulo <= 360) {
    x_atual = raio * cos(angulo * M_PI / 180);
    y_atual = raio * sin(angulo * M_PI / 180);
    delta_x = x_atual - x;
    delta_y = y_atual - y;
    
    desenhaDiagonal(delta_x, delta_y);
    delay(delay_circulo);

    angulo += angle_step;
    x = x_atual;
    y = y_atual;
  }
  sobeCaneta();
}

void desenhaCirculo() {
  int raio = 100;
  int delay_time = 50;

  sobeCaneta();

  direita(50 + 2*raio);  //indo para a posição inicial para desenhar o X
  delay(1000);
  baixo(50+raio);

  desceCaneta();

  int angulo = 0;
  int x = raio * cos(angulo * M_PI / 180);
  int y = raio * sin(angulo * M_PI / 180);
  int x_atual, delta_x;
  int y_atual, delta_y;
  while (angulo <= 360) {
    x_atual = raio * cos(angulo * M_PI / 180);
    y_atual = raio * sin(angulo * M_PI / 180);
    delta_x = x_atual - x;
    delta_y = y_atual - y;

    if (abs(delta_x) >= abs(delta_y)) {
      if (delta_y >= 0) {
        cima(delta_y);
      } else {
        baixo(abs(delta_y));
      }
      delay(delay_time);
      if (delta_x >= 0) {
        direita(delta_x);
      } else {
        esquerda(abs(delta_x));
      }
      delay(delay_time);
    } else {
      if (delta_x >= 0) {
        direita(delta_x);
      } else {
        esquerda(abs(delta_x));
      }
      delay(delay_time);
      if (delta_y >= 0) {
        cima(delta_y);
      } else {
        baixo(abs(delta_y));
      }
      delay(delay_time);
    }
    angulo += 10;
    x = x_atual;
    y = y_atual;
  }

  delta_y = 0 - y_atual;
  delta_x = raio - x_atual;
  if (delta_y >= 0) {
    cima(delta_y);
  } else {
    baixo(abs(delta_y));
  }
  delay(delay_time);
  if (delta_x >= 0) {
    direita(delta_x);
  } else {
    esquerda(abs(delta_x));
  }
  delay(delay_time);

  sobeCaneta();


  esquerda(50 + 2*raio);  //indo para a posição inicial para desenhar o X
  delay(1000);
  cima(50 + raio);
}

void desenhaCirculo2() {
  int raio = 100;
  int delay_time = 0;

  sobeCaneta();

  direita(50 + 2*raio);  //indo para a posição inicial para desenhar o X
  delay(1000);
  baixo(50+raio);

  desceCaneta();

  int angulo = 0;
  int x = raio * cos(angulo * M_PI / 180);
  int y = raio * sin(angulo * M_PI / 180);
  int x_atual, delta_x;
  int y_atual, delta_y;
  while (angulo <= 360) {
    x_atual = raio * cos(angulo * M_PI / 180);
    y_atual = raio * sin(angulo * M_PI / 180);
    delta_x = x_atual - x;
    delta_y = y_atual - y;
    if (abs(delta_x) >= abs(delta_y)) {
      if (delta_y >= 0) {
        cima(delta_y);
      } else {
        baixo(abs(delta_y));
      }
      delay(delay_time);
      if (delta_x >= 0) {
        direita(delta_x);
      } else {
        esquerda(abs(delta_x));
      }
      delay(delay_time);
    } else {
      if (delta_x >= 0) {
        direita(delta_x);
      } else {
        esquerda(abs(delta_x));
      }
      delay(delay_time);
      if (delta_y >= 0) {
        cima(delta_y);
      } else {
        baixo(abs(delta_y));
      }
      delay(delay_time);
    }
    angulo += 10;
    x = x_atual;
    y = y_atual;
  }
  delta_y = 0 - y_atual;
  delta_x = raio - x_atual;
  if (delta_y >= 0) {
    cima(delta_y);
  } else {
    baixo(abs(delta_y));
  }
  delay(delay_time);
  if (delta_x >= 0) {
    direita(delta_x);
  } else {
    esquerda(abs(delta_x));
  }
  delay(delay_time);

  sobeCaneta();


  esquerda(50 + 2*raio);  //indo para a posição inicial para desenhar o X
  delay(1000);
  cima(50 + raio);
}


//altura -> 2200 passos
//largura -> 1000 passos

//servo ->15 graus : escrita
//      ->40 graus : movimentação

//Observador olhando perto do Motor Y
//2 antihorario4p-> cima
//2 horario-> baixo
//X horario e Y antihorario-> direita
//Y horario e X antihorario-> esquerda
//X horario-> Baixo direita
//X antihorario-> Cima esquerda
//Y horario->Baixo esquerda
//Y antihorario->Cima direita
