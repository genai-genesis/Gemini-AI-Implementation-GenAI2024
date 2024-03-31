import React, { useEffect, useState } from 'react';
import { View, StyleSheet, Dimensions } from 'react-native';
import BackgroundImage from '../components/Background';

const HomeScreen = () => {
  const screenHeight = Dimensions.get('window').height; // Get the screen height
  const [gridMargin, setGridMargin] = useState(0);

  // Calculate the number of pixels from the bottom to the 34% point
  const pixelsFromBottom = screenHeight * 0.34;

  useEffect(() => {
    // Set the distance between the grid to 10% of the calculated distance
    setGridMargin(pixelsFromBottom * 0.10);
  }, []);

  return (
    <BackgroundImage backgroundImage={require('../assets/pantry2.png')}>
      <View style={styles.container}>
        <View style={styles.outerGrid}>
          {[...Array(4).keys()].map((row) => (
            <View key={row} style={styles.row}>
              <View style={styles.innerGrid}>
                {[...Array(4).keys()].map((col) => (
                  <View key={col} style={[styles.gridItem, { width: 60, height: 60, marginHorizontal: gridMargin }]} />
                ))}
              </View>
            </View>
          ))}
        </View>
      </View>
    </BackgroundImage>
  );
};

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    alignItems: 'center',
    bottom: '34%',
    left: 0,
    right: 0,
    top: "10%",
  },
  outerGrid: {
    flexDirection: 'column',
  },
  row: {
    flexDirection: 'row',
  },
  innerGrid: {
    flexDirection: 'row',
  },
  gridItem: {
    backgroundColor: 'red',
    marginTop: 50,
  },
});

export default HomeScreen;