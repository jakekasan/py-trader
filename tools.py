def smooth_data(data,window=2):
    temp = [sum(data[(i-window):(i)])/window for i in range(window,(len(data)+1))]
    prepend = [sum(data[:x])/x for x in range(1,window)]
    return(prepend+temp)
