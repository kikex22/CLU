import os
import pickle
import torch



class MemoryM:
 def __init__(self,dir=None):
    self.dir=dir or os.path.dirname(os.path.abspath(__file__))

 def SaveM(self,model,path="model/clu_model.pth"):
    path=os.path.join(self.dir,path)
    torch.save(model.state_dict(),path)
    print(f" Model guardado en {path}")

 def LoadM(self,model,path="model/clu_model.pth"):
    path=os.path.join(self.dir,path)
    if os.path.exists(path):
        model.load_state_dict(torch.load(path))
        print("Clu Activado")
    else:
        print("Clu no encontrado, se entrenara de nuevo")

 def save_paths_and_mazes(self,paths, mazes, filename="memory/multi_paths_and_mazes.pkl"):
    filepath = os.path.join(self.dir, filename)
    with open(filepath, "wb") as f:
        pickle.dump((paths, mazes), f)
    print(f"Rutas y laberintos guardados: {len(paths)}")

 def load_paths_and_mazes(self,filename="memory/multi_paths_and_mazes.pkl"):
    filepath = os.path.join(self.dir, filename)
    if not os.path.exists(filepath):
        print("No se encontraron rutas y laberintos guardados.")
        return None, None
    with open(filepath, "rb") as f:
        paths, mazes = pickle.load(f)
    print(f"Rutas y laberintos cargados: {len(paths)}")
    return paths, mazes
 