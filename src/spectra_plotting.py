import numpy as np
import matplotlib.pyplot as plt 
import os
import re

# this script demonstrates a scatter plot of peak intensities w text
#path = 'Best_Raw_Spectra_June/'
path = 'Feb-May_2021_Spectra/'

files = [f for f in os.listdir(path) if f.endswith('csv')]
out_dir = 'figs_feb_may_2021_spectra/'

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

titles = []
peak_wavelengths = []
peak_intensities = []

for f in files:

    print(f)
    # load spectrum
    spectrum = np.loadtxt(path + f, delimiter = ',')  
    
    # reading data from file name and
    # text wrangling to create title
    title_text = f[9:-12].replace('_', ' ')
    title_tokens = re.split('-|_| ', title_text)

    try:
        integration_time = float(title_tokens[-2][:-1])
    except:
        integration_time = 1

    title = '-'.join(re.split('-|_| ', title_text)[:-2])
    titles.append(title)
    
    # normalize spectra
    spectrum[:,1:] = spectrum[:,1:]/integration_time

    # plotting
    plt.title(title)
    for i in range(1,288):
        plt.plot(spectrum[:,0],spectrum[:,i])
        plt.xlim([300,800])
        plt.ylim([0,70000/integration_time])
    plt.ylabel('Intensity (counts)')
    plt.xlabel('Wavelength (nm)')

    # peak finding
    raw_peak_index = np.argmax(spectrum[:,1:])
    peak_index = np.unravel_index(raw_peak_index, spectrum[:,1:].shape)
    peak_wavelengths.append(spectrum[peak_index[0],0])
    peak_intensities.append(np.max(spectrum[:,1:]))

    plt.savefig((out_dir + f)[:-4] + '.png')
    plt.clf()
    
    # FWHM
    import scipy.signal
    FWHM = scipy.signal.peak_widths(spectrum[peak_index[0], 1:],
            [peak_index[1]])
    #print(FWHM)

# plot scatter of peak intensities w text
peak_intensities = np.asarray(peak_intensities)
normaliz_peak_intensities = peak_intensities/np.max(peak_intensities)
peak_wavelengths = np.asarray(peak_wavelengths)

plt.figure(figsize=(7, 6))
plt.scatter(peak_wavelengths, normaliz_peak_intensities, s = 10)
for w, i, t in zip(peak_wavelengths, normaliz_peak_intensities, titles):
    if w < 500 and w > 475:
        continue
    if i < 0.02:
        continue
    plt.text(w, i, t, ha = 'center', fontsize=8)

plt.savefig('test.png')
