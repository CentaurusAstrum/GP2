
def circle_sum(arr: np.ndarray, center_x, center_y, r):
    subdivisions = 100
    total = 0

    for theta in np.linspace(0, np.pi, num=subdivisions):
        x = int(np.round(center_x + r * np.cos(theta)))
        y = int(np.round(center_y + r * np.sin(theta)))
        total += arr[y, x]

    return tota l /subdivisions