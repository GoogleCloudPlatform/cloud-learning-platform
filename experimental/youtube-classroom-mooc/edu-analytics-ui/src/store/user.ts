// https://github.com/pmndrs/zusta
import create from 'zustand'

//import { User } from 'firebase/auth'

interface IUserState {
  user: null | any;
  setUser: (user: null | any) => void;
}

const useStore = create<IUserState>(set => ({
  user: null,
  setUser: (user) => set({ user }),
}))

export default useStore
