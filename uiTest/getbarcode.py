import cv2

from pyzbar import pyzbar

def read_barcode():
    cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

    barcode_set = set()
    while True:
        barcodeData = ' '
        x, y, w, h = 0, 0, 0, 0
        ret, frame = cap.read()

        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            x, y, w, h = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            barcodeData = barcode.data.decode("utf-8")
            cv2.putText(frame, barcodeData, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            barcode_set.add(barcodeData)
            print("[INFO] barcode: {}".format(barcodeData))

        cv2.imshow('cam', frame)
        k = cv2.waitKey(1)
        if k == 27:
            cv2.destroyAllWindows()
            break

    return barcode_set
