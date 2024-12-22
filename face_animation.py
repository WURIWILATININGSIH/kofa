import cv2
import numpy as np


def animate_cat_face(frame, face_coords, mouth_open_factor):
    """Animasi wajah kucing dengan kumis."""
    x, y, w, h = face_coords
    face_center = (x + w // 2, y + h // 2)
    enlarged_w = int(w * 1.2)
    enlarged_h = int(h * 1.2)

    # Wajah (lingkaran)
    cv2.circle(frame, face_center, enlarged_w // 2, (255, 200, 200), -1)

    # Mata (lingkaran hitam kecil)
    eye_radius = w // 10
    eye_offset_x = w // 5
    eye_offset_y = h // 5
    cv2.circle(frame, (face_center[0] - eye_offset_x, face_center[1] - eye_offset_y), eye_radius, (0, 0, 0), -1)
    cv2.circle(frame, (face_center[0] + eye_offset_x, face_center[1] - eye_offset_y), eye_radius, (0, 0, 0), -1)

    # Mulut (membuka sesuai pitch)
    mouth_width = int(w // 4)
    mouth_height = int(mouth_open_factor * h // 8)
    mouth_top = face_center[1] + h // 6
    mouth_left = face_center[0] - mouth_width // 2
    mouth_right = face_center[0] + mouth_width // 2
    cv2.rectangle(frame, (mouth_left, mouth_top), (mouth_right, mouth_top + mouth_height), (255, 0, 0), -1)

    # Kumis (garis-garis di sisi kiri dan kanan mulut)
    whisker_length = w // 3
    whisker_thickness = 2
    cv2.line(frame, (mouth_left - 10, mouth_top + 10),
             (mouth_left - whisker_length, mouth_top), (0, 0, 0), whisker_thickness)
    cv2.line(frame, (mouth_right + 10, mouth_top + 10),
             (mouth_right + whisker_length, mouth_top), (0, 0, 0), whisker_thickness)

    return frame


def animate_angry_face(frame, face_coords, mouth_open_factor):
    """Animasi wajah marah dengan alis menurun."""
    x, y, w, h = face_coords
    face_center = (x + w // 2, y + h // 2)

    # Wajah (lingkaran merah)
    cv2.circle(frame, face_center, w // 2, (0, 0, 255), -1)

    # Mata (lingkaran hitam)
    eye_radius = w // 10
    eye_offset_x = w // 5
    eye_offset_y = h // 5
    cv2.circle(frame, (face_center[0] - eye_offset_x, face_center[1] - eye_offset_y), eye_radius, (0, 0, 0), -1)
    cv2.circle(frame, (face_center[0] + eye_offset_x, face_center[1] - eye_offset_y), eye_radius, (0, 0, 0), -1)

    # Alis (garis miring ke bawah)
    eyebrow_thickness = 3
    eyebrow_length = w // 6
    cv2.line(frame, (face_center[0] - eye_offset_x - eyebrow_length, face_center[1] - eye_offset_y - 10),
             (face_center[0] - eye_offset_x + eyebrow_length, face_center[1] - eye_offset_y - 20), (0, 0, 0), eyebrow_thickness)
    cv2.line(frame, (face_center[0] + eye_offset_x - eyebrow_length, face_center[1] - eye_offset_y - 20),
             (face_center[0] + eye_offset_x + eyebrow_length, face_center[1] - eye_offset_y - 10), (0, 0, 0), eyebrow_thickness)

    # Mulut (terbuka sesuai pitch)
    mouth_width = int(w // 4)
    mouth_height = int(mouth_open_factor * h // 6)
    mouth_top = face_center[1] + h // 4
    mouth_left = face_center[0] - mouth_width // 2
    mouth_right = face_center[0] + mouth_width // 2
    cv2.rectangle(frame, (mouth_left, mouth_top), (mouth_right, mouth_top + mouth_height), (0, 0, 0), -1)

    return frame


def animate_girl_face(frame, face_coords, mouth_open_factor):
    """Animasi wajah feminin dengan lipstik dan pipi merah muda."""
    x, y, w, h = face_coords
    face_center = (x + w // 2, y + h // 2)

    # Wajah (lingkaran kuning)
    cv2.circle(frame, face_center, w // 2, (255, 255, 0), -1)

    # Mata (lingkaran hitam kecil)
    eye_radius = w // 12
    eye_offset_x = w // 5
    eye_offset_y = h // 5
    cv2.circle(frame, (face_center[0] - eye_offset_x, face_center[1] - eye_offset_y), eye_radius, (0, 0, 0), -1)
    cv2.circle(frame, (face_center[0] + eye_offset_x, face_center[1] - eye_offset_y), eye_radius, (0, 0, 0), -1)

    # Pipi (lingkaran merah muda)
    blush_radius = w // 10
    blush_offset_y = h // 8
    cv2.circle(frame, (face_center[0] - eye_offset_x, face_center[1] + blush_offset_y), blush_radius, (255, 182, 193), -1)
    cv2.circle(frame, (face_center[0] + eye_offset_x, face_center[1] + blush_offset_y), blush_radius, (255, 182, 193), -1)

    # Mulut (membuka sesuai pitch, lipstik merah)
    mouth_width = int(w // 4)
    mouth_height = int(mouth_open_factor * h // 8)
    mouth_top = face_center[1] + h // 6
    mouth_left = face_center[0] - mouth_width // 2
    mouth_right = face_center[0] + mouth_width // 2
    cv2.rectangle(frame, (mouth_left, mouth_top), (mouth_right, mouth_top + mouth_height), (255, 0, 0), -1)

    return frame
