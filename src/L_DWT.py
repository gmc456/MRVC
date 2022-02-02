# Este módulo está en desuso. Básicamente gestiona el desplazamiento
# de las componentes al rango de números naturales y obliga a usar 16
# bits/componente, cuando esto en realidad depende del contexto.

''' MRVC/L_DWT.py

Provides:

1. DWT LL I/O. '''

import numpy as np
import DWT
import cv2
import colored
if __debug__:
    import os

MIN = -10000 #-32768
MAX = 10000 #32767
OFFSET = 32768

def read(prefix: str, image_number: int) -> np.ndarray: # [row, column, component]
    fn = f"{prefix}F{image_number:03d}LL.png"
    if __debug__:
        print(colored.fore.GREEN + f"L.read({fn})", end=' ')
    subband = cv2.imread(fn, cv2.IMREAD_UNCHANGED)
    #subband = cv2.cvtColor(subband, cv2.COLOR_BGR2RGB)
    if __debug__:
        print(f"shape={subband.shape} dtype={subband.dtype} length={os.path.getsize(fn)}{colored.style.RESET}")
    #subband = subband.astype(np.int32)
    subband = np.array(subband, dtype=np.int32)
    subband -= OFFSET
    return subband.astype(np.int16)

def write(subband: np.ndarray, prefix: str, image_number: int) -> None:
    fn = f"{prefix}F{image_number:03d}LL.png"
    if __debug__:
        print(f"{colored.fore.GREEN}L_DWT.write({prefix}, {image_number})", end=' ')
        print(f"file={fn} max={subband.max()} min={subband.min()} shape={subband.shape} dtype={subband.dtype}", end=' ')
    #subband = subband.astype(np.int32)
    subband = np.array(subband, dtype=np.int32)
    subband += OFFSET
    assert (subband < 65536).all()
    assert (subband > -1).all()
    subband = subband.astype(np.uint16)
    #subband = cv2.cvtColor(subband, cv2.COLOR_RGB2BGR)
    cv2.imwrite(fn, subband)
    if __debug__:
        print(f"{colored.fore.GREEN}length={os.path.getsize(fn)}{colored.style.RESET}")

###############
        
def __write(subband: np.ndarray, fn:str) -> None:
    if __debug__:
        print(f"L.write({prefix}, {fn})", subband.max(), subband.min(), subband.shape, subband.dtype, end=' ')
    subband = np.array(subband, dtype=np.int32)
    subband += OFFSET
    assert (subband < 65536).all()
    assert (subband > -1).all()
    subband = subband.astype(np.uint16)
    subband = cv2.cvtColor(subband, cv2.COLOR_RGB2BGR)
    fn = fn + ".png"
    cv2.imwrite(fn, subband)
    if __debug__:
        print(os.path.getsize(fn))

def __read(fn:str) -> np.ndarray: # [row, column, component]
    fn = fn + ".png"
    subband = cv2.imread(fn, cv2.IMREAD_UNCHANGED)
    subband = cv2.cvtColor(subband, cv2.COLOR_BGR2RGB)
    if __debug__:
        print(f"L.read({prefix}, {image_number})", subband.shape, subband.dtype, os.path.getsize(fn))
    #subband = subband.astype(np.int32)
    subband = np.array(subband, dtype=np.int32)
    subband -= OFFSET
    return subband#.astype(np.int16)

def __read(prefix: str, image_number: int) -> np.ndarray: # [row, column, component]
    #ASCII_image_number = str(image_number).zfill(3)
    fn = f"{prefix}LL{image_number:03d}.png"
    #fn = name + ".png"
    subband = cv2.imread(fn, cv2.IMREAD_UNCHANGED)
    #try:
    #    L = cv2.cvtColor(L, cv2.COLOR_BGR2RGB)
    #except cv2.error:
    #    print(colors.red(f'L.read: Unable to read "{fn}"'))
    #    raise
    if __debug__:
        print(f"L.read({prefix}, {image_number})", subband.shape, subband.dtype, os.path.getsize(fn))
    #L_int32 = np.array(L, dtype=np.int32)
    subband = np.array(subband, dtype=np.float64)
    #tmp = np.array(L.shape, dtype=np.
    #subband = np.array(subband, dtype=np.float64)
    #assert L.dtype == np.int16
    subband -= OFFSET
    #L -= 32768
    #L = L.astype(np.uint16)
    return subband#.astype(np.int16)

def __write(subband: np.ndarray, prefix: str, image_number: int) -> None:
    if __debug__:
        print(f"L.write({prefix}, {image_number})", L.shape, L.dtype, end=' ')
    #subband = np.array(L, dtype=np.float64)
    assert subband.all() <= MAX
    assert subband.all() >= MIN
    #L_int32 = np.array(L, dtype=np.int32)
    subband = np.array(L, dtype=np.float64)
    #L_int32 = L.astype(np.float32)
    subband += OFFSET
    #L += 32768
    #subband += 32768.0
    L = L.astype(np.uint16)
    #ASCII_image_number = str(image_number).zfill(3)
    #fn = name + ".png"
    #L = cv2.cvtColor(L, cv2.COLOR_RGB2BGR)
    fn = f"{prefix}LL{image_number:03d}.png"
    cv2.imwrite(fn, L)
    if __debug__:
        print(os.path.getsize(fn))

def interpolate(L: np.ndarray) -> np.ndarray:
    LH = np.zeros(shape=L.shape, dtype=np.float64)
    HL = np.zeros(shape=L.shape, dtype=np.float64)
    HH = np.zeros(shape=L.shape, dtype=np.float64)
    H = (LH, HL, HH)
    _L_ = DWT.synthesize_step(L, H)
    return _L_

def reduce(_L_: np.ndarray) -> np.ndarray:
    L, _ = DWT.analyze_step(_L_)
    return L
