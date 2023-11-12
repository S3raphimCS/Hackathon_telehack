export interface IUserSignIn {
  email: string;
  password: string;
}

export interface ITokens {
  access: string;
  refresh: string;
}

export interface IUser {
  id: number;
  email: string;
  avatar: string;
  first_name: string;
  second_name: string;
  middle_name: string;
}
