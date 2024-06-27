import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Points de départ et d'arrivée
start_point = np.array([3, 5, 3])
end_point = np.array([4, 5, 3])


# Fonction pour générer des points sur un arc de cercle
def generate_arc(start, end, num_points=50):
    # Vecteur directeur
    dir_vector = end - start
    print(dir_vector)

    # Trouver le centre de l'arc de cercle
    center = (start + end) / 2

    # Vecteur orthogonal
    orth_vector = np.cross(dir_vector, np.array([0, 1, 0]))

    # Normaliser le vecteur orthogonal
    orth_vector = orth_vector / np.linalg.norm(orth_vector)

    # Rayon de l'arc
    radius = np.linalg.norm(dir_vector) / 2

    # Créer les points sur l'arc
    theta = np.linspace(0, np.pi, num_points)
    arc_points = np.zeros((num_points, 3))
    for i, t in enumerate(theta):
        arc_points[i] = center + radius * (
                    np.cos(t) * dir_vector / np.linalg.norm(dir_vector) + np.sin(t) * orth_vector)

    return arc_points


# Générer les points sur l'arc de cercle
arc_points = generate_arc(start_point, end_point)
print( arc_points)
# Tracer l'arc de cercle
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(arc_points[:, 0], arc_points[:, 1], arc_points[:, 2], label='Arc de cercle')
ax.scatter(start_point[0], start_point[1], start_point[2], color='r', label='Point de départ')
ax.scatter(end_point[0], end_point[1], end_point[2], color='g', label='Point d\'arrivée')
ax.legend()

plt.show()
