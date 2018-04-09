def Density(temp, pres):
    Rgas = 287.058
    density = pres/(Rgas*temp)
    return density

print(Density(1,2))
