import hashlib

class hasher:
    def __init__(self, fileLocation):
        self.fileLocation = fileLocation


    def hash(self, value):
        hashedString = hashlib.sha256(str(value).encode()).hexdigest()
        #print("Hashed to:" , hashedString)
        return(hashedString)

    def doesHashExistInDatabase(self, hash):
        hashInFile = False
        with open(self.fileLocation, 'r') as file:
            for line in file:
                # Convert each line (number) to a string
                line = line.strip()
                
                # Check if the target hash is in the string representation of the number
                if str(hash) == line:
                    hashInFile = True

        return hashInFile

    
    def addHashToDatabase(self, hash):
        with open(self.fileLocation, 'a') as file:
            file.write(str(hash) + "\n")

    def addToDatabaseIfNotExist(self, value):
        wasHashInFile = True
        hashed_Value = self.hash(value)
        if(not self.doesHashExistInDatabase(hashed_Value)):
            self.addHashToDatabase(hashed_Value)
            wasHashInFile = False


        
        return wasHashInFile


    
