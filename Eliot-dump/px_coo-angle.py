from geometry_msgs.msg import Point


def px_coo_to_angle(self, px_coo, device):
#data specifiques pour chaque cameras
    if device == "camera":
        hfov = 69
        vfov = 42
        hpx = 848
        vpx = 480
    if device == "depth":
        hfov = 87
        vfov = 58
        hpx = 848
        vpx = 480

    # Un angle c'est un Point car tamer
    # angle.x est l'angle longitudinal qui nous intéresse calculé par rapport au pixel de camera
    # angle.y est l'angle de la hauteur 
    if hfov is not None:
        angle = Point()
        angle.x = (px_coo.x - hpx/2)/hpx*hfov/2 # calcul : coordonée 0 mise au centre pour avoir +- largeur image en coo
        angle.y = (px_coo.y - vpx/2)/vpx*vfov/2 # coo ratoinalisée par la largeur totale multipliée par angle fov/2 pour chaque côté
        angle.z = 0.0 # Zéro
        return angle
    return None #apas marché car device pas reconnu