

def discrete_colorscale(bvals, colors):
    """
    This function creates a discrete colormap. Taken from https://bit.ly/4cLYjQe
    bvals - list of values bounding intervals/ranges of interest
    colors - list of rgb or hex colorcodes for values in [bvals[k], bvals[k+1]],0<=k < len(bvals)-1
    returns the plotly  discrete colorscale
    """
    if len(bvals) != len(colors)+1:
        raise ValueError(
            'len(boundary values) should be equal to  len(colors)+1')
    bvals = sorted(bvals)
    nvals = [(v-bvals[0])/(bvals[-1]-bvals[0])
             for v in bvals]  # normalized values

    dcolorscale = []  # discrete colorscale
    for k in range(len(colors)):
        dcolorscale.extend([[nvals[k], colors[k]], [nvals[k+1], colors[k]]])
    return dcolorscale
