void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  int max_sound = 1234;
  String string_sound = String(max_sound);
  string_sound.trim();
  Serial.println("\n\n");
  Serial.println(string_sound);
}

void loop() {
  // put your main code here, to run repeatedly:

}
