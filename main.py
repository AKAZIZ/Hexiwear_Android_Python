################################################################################
# ble_final
# Created at 2018-03-12 21:29:47.291436
# Made by: Danni Liu
################################################################################

# Importer pour Bluetooth
from nxp.hexiwear.kw40z import kw40z
import streams
import threading

streams.serial()

# Fonction pour Button gauche
def toggle_ble(): 
    try:
        # Quand taper Button gauche, il va afficher "Left Button Pressed" dans le COMS
        print("Left Button Pressed") 
        # Changer le statut du processus de publicité. Active / désactive l'état Bluetooth
        bt_driver.toggle_adv_mode()
    except Exception as e:
        print("error on left_pressed", e)
        
# Fonction pour connecter par code
def print_paircode():
    # Il génère un code d'appariement stocké dans l'attribut de classe de clé d'accès
    print("Your Pair Code:",bt_driver.passkey)

# Configurer LED1 en mode OUTPUT, on peut l'allumer et l'éteindre
pinMode(LED1, OUTPUT)

# Fonction pour vérifier l'état du bluetooth
def check_status():
    print("Device Settings")
    # Récupère les informations de la bluetooth
    # Bluetooth Status (bool): 1 Bluetooth est activé, 0 Bluetooth est désactivé;
    # Boutons tactiles capacitifs (bool): 1 paire droite active, 0 paire gauche active;
    # Link Status (bool): 1 appareil est connecté, 0 appareil est déconnecté.
    bt_on, bt_touch, bt_link = bt_driver.info()
    print("Bluetooth State: ", ("On" if bt_on == 1 else "Off"))
    # LED pour indiquer l'état de Bluetooth
    digitalWrite(LED1, 0 if bt_on==1 else 1)
    print("Capacitive Button Active: ", ("Left" if bt_touch == 0 else "Right"))
    print("Link State: ", ("Connected" if bt_link == 1 else "Disconnected"))
    # Boucle pour toujours
    # Mise à jour l'état de Bluetooth
    while True:
        bt_on_new, bt_touch_new, bt_link_new = bt_driver.info()
        if bt_on_new != bt_on:
            print("Bluetooth State: ", ("On" if bt_on_new == 1 else "Off"))
            digitalWrite(LED1, 0 if bt_on_new==1 else 1)
            bt_on = bt_on_new
        if bt_touch_new != bt_touch:
            print("Capacitive Button Active: ", ("Left" if bt_touch_new == 0 else "Right"))
            bt_touch = bt_touch_new
        if bt_link_new != bt_link:
            print("Link State: ", ("Connected" if bt_link_new == 1 else "Disconnected"))
            bt_link = bt_link_new
        sleep(500)
        
try:
    # Configurer la puce ble
    print("init...")
    bt_driver = kw40z.KW40Z_HEXI_APP(SERIAL1)
    print("start")
    # Démarrer la communication série avec le KW40Z
    # Vérifier l'état du KW40Z:
    # Vérifier si le Bluetooth est actif
    # Vérifier s'il y a des connexions avec d'autres appareils
    # Vérifier quel bouton est actif
    bt_driver.start()
    # Attendre le démarrage de la puce ble
    sleep(1000)
    # Démarrer thread pour vérifier le statut
    thread(check_status)
    # Attacher la fonction de rappel au bouton gauche
    bt_driver.attach_button_left(toggle_ble)
    bt_driver.attach_passkey(print_paircode)
except Exception as e:
    print("error1:", e)
    
# Détecter et envoyer les données de capteurs
level = 0
while True:
    try:
        print("...")
        # Mise à jour les données des capteurs Hexiwear de la puce KW40Z
        # Batterie - met à jour la valeur du niveau de la batterie en pourcentage
        bt_driver.upd_sensors(battery=level)
        # Tous les 5000 incréments jusqu'au 100
        level += 1
        if level > 100:
            level = 0
        sleep(5000)
    except Exception as e:
        print("error2", e)
        sleep(1000)
