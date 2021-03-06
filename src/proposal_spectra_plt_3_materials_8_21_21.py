import numpy as np
import matplotlib.pyplot as plt 
import os
import re

# this is a script that demonstrates some of the plotting we've done on the project

out_dir = 'out/proposal_plotting_8_21_21/'

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

titles = []
peak_wavelengths = []
peak_intensities = []


def plot_group(files, group_title, xlim):
    colors = iter(('c','m','y'))
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


        # peak finding
        raw_peak_index = np.argmax(spectrum[:,1:])
        peak_index = np.unravel_index(raw_peak_index, spectrum[:,1:].shape)
        peak_wl = spectrum[peak_index[0],0]
        peak_wavelengths.append(spectrum[peak_index[0],0])
        peak_intensities.append(np.max(spectrum[:,1:]))
        
        # plotting
        clr = next(colors)
        plt.plot(spectrum[:,0],spectrum[:,peak_index[1] + 1], color = clr)
        plt.xlim(xlim)
        #plt.ylim([0,70000/integration_time])
        plt.ylabel('Intensity (counts)')
        plt.xlabel('Wavelength (nm)')

        plt.axvline(x = peak_wl,
                label = title + ': \n peak at ' + str(round(peak_wl, 2)) + ' nm', 
                ls='--',
                color = clr)
        
        # secondary peak
        #if == '20210616_4OH-PEABr_PbBr2_15k_573_spectra.csv':
        #    2nd_peak_index = np.unravel_index(raw_peak_index,
        #            spectrum[:,1:].shape)

        plt.legend()

        # FWHM
        import scipy.signal
        FWHM = scipy.signal.peak_widths(spectrum[peak_index[0], 1:],
                [peak_index[1]])

    title = "Shifts in Emission Wavelength in Functionalized {} Derivatives"
    plt.title(title.format(group_title))
    plt.savefig(out_dir + group_title + '_selected_spectra_max_intensities' + '.png')
    plt.clf()


#############################################################################

path = 'data/Best_Raw_Spectra_June/'

content = [
        {"group_title" : 'PEABr',
            "files" : ['20210616_(4MeOPEABr)2-PbBr2_4k_572_spectra.csv',
            '20210601_(PEABr)2-PbBr2_4k_544_spectra.csv'], #'20210616_4OH-PEABr_PbBr2_15k_573_spectra.csv']
            "xlim" : [380, 460]},
        {"group_title" :'PEAI',
            "files" : ['20210616_(4MeOPEAI)2-PbI2_4k_570_spectra.csv',
            '20210601_(PEAI)2-PbI2_4k_543_spectra.csv'], #'20210608_(4OHPEAI)2-PbI2_200K_559_spectra.csv']
            "xlim" : [475, 600]},
        {"group_title" :'FPEAI',
            "files" : ['20210608_(4FPEAI)2-PbI2_200k_561_spectra.csv',
            '20210603_(3FPEAI)2-PbI2_500k_549_spectra.csv'], #'20210608_(4OHPEAI)2-PbI2_200K_559_spectra.csv']
            "xlim" : [400, 600]},
        ]

#20210608_(4FPEAI)2-PbI2_200k_561_spectra.csv
#20210603_(3FPEAI)2-PbI2_500k_549_spectra.csv

for d in content:
    plot_group(d['files'],
            d['group_title'], 
            d['xlim'])

