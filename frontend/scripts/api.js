const base_url = 'https://ws.geonorge.no/transformering/v1/';

// Retrieves a list of available coordinate projections from a web service
async function getAvailableProjections() {
    const url = `${base_url}/projeksjoner`;
    const response = await fetch(url);
    const projections = await response.json();
    return projections;
}

// Transforms a single set of coordinates from one projection to another
async function transformSingleCoordinate(x, y, from_epsg, to_epsg) {
    const url = `${base_url}/transformer?x=${x}&y=${y}&fra=${from_epsg}&til=${to_epsg}`;
    const response = await fetch(url);
    const transformedCoordinate = await response.json();
    return transformedCoordinate;
}

// This function transforms an array of coordinates from one projection to another
async function transformMultipleCoordinates(coordinates, from_epsg, to_epsg) {
    const transformedCoordinates = [];
    for (const coordinate of coordinates) {
        const transformedCoordinate = await transformSingleCoordinate(
            coordinate.x,
            coordinate.y,
            from_epsg,
            to_epsg
        );
        transformedCoordinates.push(transformedCoordinate);
    }
    return transformedCoordinates;
}

// This function checks if the input is an array of coordinates and transforms them accordingly
async function transformCoordinates(coordinates, from_epsg, to_epsg) {
    if (!Array.isArray(coordinates) || coordinates.length === 0) {
        throw new Error('Invalid coordinates array');
    }

    if (coordinates.length === 1) {
        const { x, y } = coordinates[0];
        const transformedCoordinate = await transformSingleCoordinate(x, y, from_epsg, to_epsg);
        return [transformedCoordinate];
    }

    return transformMultipleCoordinates(coordinates, from_epsg, to_epsg);
}


// Export the functions as an object so that they can be used in other modules
module.exports = {
    getAvailableProjections,
    transformCoordinates,
    updateCoordinates
};
