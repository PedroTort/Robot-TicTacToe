#include <Servo.h>

Servo myservo; 
int posMaxCaneta = 40;
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

//A498
int delayTime = 300;
int stps=10;

void cima(int steps)
{
  digitalWrite(X_DIR, false);
  digitalWrite(Y_DIR, false);
  
  for (int i = 0; i< steps; i++)
  {
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

void baixo(int steps)
{
  digitalWrite(X_DIR, true);
  digitalWrite(Y_DIR, true);
  
  for (int i = 0; i< steps; i++)
  {
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

void esquerda(int steps)
{
  digitalWrite(X_DIR, false);
  digitalWrite(Y_DIR, true);
  
  for (int i = 0; i< steps; i++)
  {
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

void direita(int steps)
{
  digitalWrite(X_DIR, true);
  digitalWrite(Y_DIR, false);
  
  for (int i = 0; i< steps; i++)
  {
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

//X horario-> Baixo direita
//X antihorario-> Cima esquerda
//Y horario->Baixo esquerda
//Y antihorario->Cima direita

void diagonalCimaDireita(int steps)
{
  for (int i = 0; i< steps; i++)
  {
    cima(1);
    delay(1);
    direita(1);
  }
   
}

void diagonalBaixoEsquerda(int steps)
{  
  for (int i = 0; i< steps; i++)
  {
    baixo(1);
    delay(1);
    esquerda(1);
  }
}


void diagonalBaixoDireita(int steps)
{ 
  for (int i = 0; i< steps; i++)
  {
    baixo(1);
    delay(1);
    direita(1);
  }
}

void diagonalCimaEsquerda(int steps)
{
  for (int i = 0; i< steps; i++)
  {
    cima(1);
    delay(1);
    esquerda(1);
  }
}

void step(boolean dir, byte dirPin, byte stepperPin, int steps)
{
  digitalWrite(dirPin, dir);
  for (int i = 0; i< steps; i++)
  {
    digitalWrite(stepperPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepperPin, LOW);
    delayMicroseconds(1000);
  }
}

void sobeCaneta(){
  if(posCaneta>=0){
    for(posCaneta;posCaneta<posMaxCaneta;posCaneta++){
//      Serial.print(posCaneta);
      myservo.write(posCaneta);     
    }}delay(500);
}

void desceCaneta(){
  if(posCaneta>=0){
    for(posCaneta;posCaneta>0;posCaneta--){
//      Serial.print(posCaneta);
      myservo.write(posCaneta);     
    }}delay(500);
}

//Inicio x = 0,y=0
void desenhaVelha(){
  sobeCaneta();
  cima(950);
  delay(500);

//  Serial.print("Posicao padrao 1: ");
//  Serial.print(posCaneta);
//  Serial.println();
  desceCaneta();
  delay(300);
  direita(900);
  delay(500);
//  Serial.print("Descida 1: ");
//  Serial.print(posCaneta);
//  Serial.println();
  
  sobeCaneta();
  cima(300);
  delay(500);
  
  desceCaneta();
//   Serial.print("Descida 2: ");
//  Serial.print(posCaneta);
//  Serial.println();
  delay(300);
  esquerda(900);
  delay(500);

  sobeCaneta();
  cima(300);
  delay(500);
  direita(300);
  delay(500);

  desceCaneta();
//    /  Serial.print("Descida 3: ");
//  /Serial.print(posCaneta);
//  /Serial.println();
  delay(300);
  baixo(900);
  delay(500);

  sobeCaneta();
  direita(300);
  delay(500);

  desceCaneta();
//      /Serial.print("Descida 3: ");
//  /Serial.print(posCaneta);
//  /Serial.println();
  delay(300);
  cima(900);
  delay(500);

  sobeCaneta();
  esquerda(700);
  baixo(1650);
}

void vaiPosicao11()
{
  sobeCaneta();
  cima(1550);
  delay(500);  
}

void voltaPosicao11()
{
  sobeCaneta();
  baixo(1550);
  delay(500);  
}

void vaiPosicao12()
{
  sobeCaneta();
  cima(1550);
  direita(300);
  delay(500);  
}

void voltaPosicao12()
{
  sobeCaneta();
  baixo(1550);
  esquerda(300);
  delay(500);  
}

void vaiPosicao13()
{
  sobeCaneta();
  cima(1550);
  direita(600);
  delay(500);  
}

void voltaPosicao13()
{
  sobeCaneta();
  baixo(1550);
  esquerda(600);
  delay(500);  
}

void vaiPosicao21()
{
  sobeCaneta();
  cima(1250);
  delay(500);  
}

void voltaPosicao21()
{
  sobeCaneta();
  baixo(1250);
  delay(500); 
}

void vaiPosicao22()
{
  sobeCaneta();
  cima(1250);
  direita(300);
  delay(500); 
}

void voltaPosicao22()
{
  sobeCaneta();
  baixo(1250);
  esquerda(300);
  delay(500); 
}

void vaiPosicao23()
{
  sobeCaneta();
  cima(1250);
  direita(600);
  delay(500);  
}

void voltaPosicao23()
{
  sobeCaneta();
  baixo(1250);
  esquerda(600);
  delay(500); 
}

void vaiPosicao31()
{
  sobeCaneta();
  cima(950);
  delay(500);
}

void voltaPosicao31()
{
  sobeCaneta();
  delay(500);
  baixo(950);
}

void vaiPosicao32()
{
  sobeCaneta();
  cima(950);
  direita(300);
  delay(500);
}

void voltaPosicao32()
{
  sobeCaneta();
  baixo(950);
  esquerda(300);
  delay(500);
}

void vaiPosicao33()
{
  sobeCaneta();
  cima(950);
  direita(600);
  delay(500);
}

void voltaPosicao33()
{
  sobeCaneta();
  baixo(950);
  esquerda(600);
  delay(500);
}


void desenhaX()
{
      direita(80);   //indo para a posição inicial para desenhar o X
      delay(1000);
      baixo(80);
      
      desceCaneta();
      diagonalBaixoDireita(141);
      delay(1000);
      
      sobeCaneta();
      esquerda(141);
      delay(1000);

      desceCaneta();
      diagonalCimaDireita(141);
      delay(1000);

      sobeCaneta();
      esquerda(141);
      delay(1000);

      
      cima(80);
      delay(1000);
      esquerda(80);
      
}

void desenhaO()
{
  sobeCaneta();
  direita(150);   //indo para a posição inicial para desenhar o O
  baixo(80);


  //primeiro quadrante
  
  desceCaneta();
  delay(200);
  
  direita(8);
  delay(50);
  baixo(1);
  delay(50);
  direita(6);
  delay(50);
  baixo(1);
  direita(6);
  delay(50);
  baixo(1);
  direita(3);
  delay(50);
  baixo(1);
  direita(3);
  delay(50);
  baixo(1);
  direita(2);
  delay(50);
  baixo(1);
  direita(2);
  delay(50);
  baixo(1);
  direita(3);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(1);
  direita(2);
  delay(50);
  baixo(1);
  direita(2);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(1);
  direita(2);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(1);
  direita(2);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(1);   //13
  direita(1);
  delay(50);
  baixo(2);
  direita(1);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(2);
  direita(1);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(2);
  direita(1);
  delay(50);
  baixo(2);
  direita(1);
  delay(50);
  baixo(1);
  direita(1);
  delay(50);
  baixo(3);
  direita(1);
  delay(50);
  baixo(2);
  direita(1);
  delay(50);
  baixo(2);
  direita(1);
  delay(50);
  baixo(3);
  direita(1);
  delay(50);
  baixo(3);
  direita(1);
  delay(50);
   baixo(5);
  direita(1);
  delay(50);
  baixo(6);
  direita(1);
  delay(50);
  baixo(16);


  // segundo quadrante
  delay(50);
  esquerda(1);
  baixo(6);
  delay(50);
  esquerda(1);
  baixo(5);
  delay(50);
  esquerda(1);
  baixo(3);
  delay(50);
  esquerda(1);
  baixo(3);
  delay(50);
  esquerda(1);
  baixo(2);
  delay(50);
  esquerda(1);
  baixo(2);
  delay(50);
  esquerda(1);
  baixo(3);
  delay(50);
  esquerda(1);
  baixo(1);
  delay(50);
  esquerda(1);
  baixo(2);
  delay(50);
  esquerda(1);
  baixo(2);
  delay(50);
  esquerda(1);
  baixo(1);
  delay(50);
  esquerda(1);
  baixo(2);
  delay(50);
  esquerda(1);
  baixo(1);
  delay(50);
  esquerda(1);
  baixo(2);
  delay(50);
  esquerda(1);
  baixo(1);
    delay(50);
  esquerda(1);
  baixo(1);
    delay(50);
  esquerda(1);
  baixo(1);
    delay(50);
  esquerda(1);
  baixo(1);
    delay(50);
  esquerda(1);
  baixo(1);
    delay(50);
  esquerda(1);
  baixo(1);
    delay(50);
  esquerda(1);
  baixo(1);
    delay(50);
  esquerda(1);
  baixo(1);
    delay(50);
  esquerda(1);
  baixo(1);
    delay(50);
  esquerda(1);
  baixo(1);
    delay(50);
  esquerda(1);
  baixo(1);
    delay(50);
  esquerda(1);
  baixo(1);
  delay(50);
  esquerda(1);
  baixo(1);
  delay(50);
  esquerda(2);
  baixo(1);
  delay(50);
  esquerda(1);
  baixo(1);
  delay(50);
  esquerda(2);
  baixo(1);
  delay(50);
  esquerda(1);
  baixo(1);
  delay(50);
  esquerda(2);
  baixo(1);
  delay(50);
  esquerda(2);
  baixo(1);
  delay(50);
  esquerda(1);
  baixo(1);
  delay(50);
  esquerda(3);
  baixo(1);
  delay(50);
  esquerda(2);
  baixo(1);
  delay(50);
  esquerda(2);
  baixo(1);
  delay(50);
  esquerda(3);
  baixo(1);
  delay(50);
  esquerda(3);
  baixo(1);
  delay(50);
  esquerda(5);
  baixo(1);
  delay(50);
  esquerda(6);
  baixo(1);
  delay(50);
  esquerda(16);
  

  //terceiro quadrante
  delay(50);
  cima(1);
  esquerda(6);
  delay(50);
  cima(1);
  esquerda(5);
  delay(50);
  cima(1);
  esquerda(3);
  delay(50);
  cima(1);
  esquerda(3);
  delay(50);
  cima(1);
  esquerda(2);
  delay(50);
  cima(1);
  esquerda(2);
  delay(50);
  cima(1);
  esquerda(3);
  delay(50);
  cima(1);
  esquerda(1);
  delay(50);
  cima(1);
  esquerda(2);
  delay(50);
  cima(1);
  esquerda(2);
  delay(50);
  cima(1);
  esquerda(1);
  delay(50);
  cima(1);
  esquerda(2);
  delay(50);
  cima(1);
  esquerda(1);
  delay(50);
  cima(1);
  esquerda(2);
  delay(50);
  cima(1);
  esquerda(1);
    delay(50);
  cima(1);
  esquerda(1);
    delay(50);
  cima(1);
  esquerda(1);
    delay(50);
  cima(1);
  esquerda(1);
    delay(50);
  cima(1);
  esquerda(1);
    delay(50);
  cima(1);
  esquerda(1);
    delay(50);
  cima(1);
  esquerda(1);
    delay(50);
  cima(1);
  esquerda(1);
    delay(50);
  cima(1);
  esquerda(1);
    delay(50);
  cima(1);
  esquerda(1);
    delay(50);
  cima(1);
  esquerda(1);
    delay(50);
  cima(1);
  esquerda(1);
  delay(50);
  cima(1);
  esquerda(1);
  delay(50);
  cima(2);
  esquerda(1);
  delay(50);
  cima(1);
  esquerda(1);
  delay(50);
  cima(2);
  esquerda(1);
  delay(50);
  cima(1);
  esquerda(1);
  delay(50);
  cima(2);
  esquerda(1);
  delay(50);
  cima(2);
  esquerda(1);
  delay(50);
  cima(1);
  esquerda(1);
  delay(50);
  cima(3);
  esquerda(1);
  delay(50);
  cima(2);
  esquerda(1);
  delay(50);
  cima(2);
  esquerda(1);
  delay(50);
  cima(3);
  esquerda(1);
  delay(50);
  cima(3);
  esquerda(1);
  delay(50);
  cima(5);
  esquerda(1);
  delay(50);
  cima(6);
  esquerda(1);
  delay(50);
  cima(16);

  // quarto quadrante
  delay(50);
  direita(1);
  cima(6);
  delay(50);
  direita(1);
  cima(5);
  delay(50);
  direita(1);
  cima(3);
  delay(50);
  direita(1);
  cima(3);
  delay(50);
  direita(1);
  cima(2);
  delay(50);
  direita(1);
  cima(2);
  delay(50);
  direita(1);
  cima(3);
  delay(50);
  direita(1);
  cima(1);
  delay(50);
  direita(1);
  cima(2);
  delay(50);
  direita(1);
  cima(2);
  delay(50);
  direita(1);
  cima(1);
  delay(50);
  direita(1);
  cima(2);
  delay(50);
  direita(1);
  cima(1);
  delay(50);
  direita(1);
  cima(2);
  delay(50);
  direita(1);
  cima(1);
    delay(50);
  direita(1);
  cima(1);
    delay(50);
  direita(1);
  cima(1);
    delay(50);
  direita(1);
  cima(1);
    delay(50);
  direita(1);
  cima(1);
    delay(50);
  direita(1);
  cima(1);
    delay(50);
  direita(1);
  cima(1);
    delay(50);
  direita(1);
  cima(1);
    delay(50);
  direita(1);
  cima(1);
    delay(50);
  direita(1);
  cima(1);
    delay(50);
  direita(1);
  cima(1);
    delay(50);
  direita(1);
  cima(1);
  delay(50);
  direita(1);
  cima(1);
  delay(50);
  direita(2);
  cima(1);
  delay(50);
  direita(1);
  cima(1);
  delay(50);
  direita(2);
  cima(1);
  delay(50);
  direita(1);
  cima(1);
  delay(50);
  direita(2);
  cima(1);
  delay(50);
  direita(2);
  cima(1);
  delay(50);
  direita(1);
  cima(1);
  delay(50);
  direita(3);
  cima(1);
  delay(50);
  direita(2);
  cima(1);
  delay(50);
  direita(2);
  cima(1);
  delay(50);
  direita(3);
  cima(1);
  delay(50);
  direita(3);
  cima(1);
  delay(50);
  direita(5);
  cima(1);
  delay(50);
  direita(5);
  cima(1);
  delay(50);
  direita(4);
  cima(1);
  delay(50);
  direita(6);
  cima(1);
  delay(50);
  direita(8);

  
  sobeCaneta();
  esquerda(150);
  cima(80);
  
  
}

void setup()
{
  pinMode(X_DIR, OUTPUT); pinMode(X_STP,OUTPUT);
  pinMode(Y_DIR, OUTPUT); pinMode(Y_STP,OUTPUT);
  pinMode(EN, OUTPUT);
  digitalWrite(EN,LOW);
  
  myservo.attach(11); 
  myservo.write(posCaneta); 
  Serial.begin(9600);
  
}

void loop()
{
  
  if (Serial.available() > 0) {
 
    incomingByte = Serial.read();
//    if(incomingByte == 'c'){        //função pra ir pra cima de 10 em 10 passos
//      cima(stps);
//      delay(1000);
//      posCima += stps;
//      Serial.print("Cima:");
//      Serial.println(posCima);
//    }
//    if(incomingByte == 'd'){        //função pra ir pra direita de 10 em 10 passos
//      direita(stps);
//      delay(1000);
//      posDireita += stps;
//      Serial.print("Direita:");
//      Serial.println(posDireita);
//    }
//    if(incomingByte == 'e'){       //função pra ir pra cima de 100 em 100 passos
//      cima(stps*10);
//      delay(1000);
//      posCima += stps*10;
//      Serial.print("Cima:");
//      Serial.println(posCima);
//    }
//    if(incomingByte == 'f'){      //função pra ir pra direita de 100 em 100 passos
//      direita(stps*10);
//      delay(1000);
//      posDireita += stps*10;
//      Serial.print("Direita:");
//      Serial.println(posDireita);
//    }
    if(incomingByte == 'a'){      //função pra subir a caneta, girando o servo de 1 em 1
      if(posCaneta<40){
        posCaneta +=1;
        myservo.write(posCaneta);
        Serial.print("Posicao Caneta:");
        Serial.println(posCaneta);
      }
      //sobeCaneta();
      //sobeCaneta();
    }
    if(incomingByte == 's'){      //função pra subir a caneta, girando o servo de 1 em 1
        posCaneta=20;
        myservo.write(posCaneta);
        Serial.print("Posicao Caneta:");
        Serial.println(posCaneta);
        
    }
    
    if(incomingByte == 'b'){      //função pra descer a caneta, girando o servo de 1 em 1
      if(posCaneta>0){
        posCaneta -=1;
        myservo.write(posCaneta);
        Serial.print("Posicao Caneta:");
        Serial.println(posCaneta);
      }
      //Serial.print("Posicao Caneta: Baixo\n");
      //desceCaneta();
    }
    
    if(incomingByte == 'r'){      //função pra subir a caneta, girando o servo de 1 em 1
        sobeCaneta();
        Serial.print("Posicao Caneta:");
        Serial.println(posCaneta);
    }

    if(incomingByte == 'd'){      //função pra subir a caneta, girando o servo de 1 em 1
        desceCaneta();
        Serial.print("Posicao Caneta:");
        Serial.println(posCaneta);
    } 
    
    if(incomingByte == 'v'){      //função pra fazer o "tabuleiro" do jogo da velha
      desenhaVelha();
    }

    if(incomingByte == 'u'){
      desenhaVelha();
      
      vaiPosicao31();
      desenhaX();
      voltaPosicao31();
      
      vaiPosicao32();
      desenhaX();
      voltaPosicao32();
      
      vaiPosicao33();
      desenhaX();
      voltaPosicao33();
      
      vaiPosicao21();
      desenhaX();
      voltaPosicao21();
      
      vaiPosicao22();
      desenhaX();
      voltaPosicao22();
      
      vaiPosicao23();
      desenhaX();
      voltaPosicao23();
      
      vaiPosicao11();
      desenhaX();
      voltaPosicao11();
      
      vaiPosicao12();
      desenhaX();
      voltaPosicao12();
      
      vaiPosicao13();
      desenhaX();
      voltaPosicao13();

    }
  }

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
