import pickle
import numpy as np
from pymatgen.core.structure import Structure

input_file = 'sampled_data.p'
output_file = 'output_file.extxyz'

# Step 1: Pickle 데이터 로드
with open(input_file, 'rb') as f:
    data = pickle.load(f)

# extxyz 형식으로 저장하기
with open('output.extxyz', 'w') as f:
    for material_id, structures in data.items():
        print(f"extract data: {material_id}")
        structure_count = len(structures['structure'])  # 구조 개수

        for i in range(structure_count):
            structure = structures['structure'][i]  # 각 구조를 선택
            positions = structure.cart_coords  # pymatgen Structure에서 positions 추출
            energies = structures['energy'][i]  # 해당 구조에 대한 energy
            forces = structures['force'][i]  # 해당 구조에 대한 force
            stresses = structures['stress'][i]  # 해당 구조에 대한 stress
            atom_species = structures['structure'][i].species 

            # 길이 검사 추가
            if len(positions) != len(forces):
                print(f"Length mismatch for material ID {material_id}, structure index {i}")
                continue  # 길이가 일치하지 않으면 건너뜁니다.

            # Lattice 정의
            lattice = structure.lattice  # pymatgen Lattice 객체
            lattice_str = " ".join(map(str, lattice.matrix.flatten()))  # Lattice를 문자열로 변환

            # Write the lattice information
            # stress 리스트를 문자열로 변환
            stress_flattened = [s for stress in stresses for s in stress]  # 스트레스를 flatten 처리
            stress_str = " ".join(map(str, stress_flattened))  # 문자열로 변환
            f.write(f"{len(positions)}\n")
            f.write(f"Lattice=\"{lattice_str}\" Properties=species:S:1:pos:R:3:forces:R:3 stress=\"{stress_str}\" energy={energies} pbc=\"T T T\"\n")


            # Write positions and forces
            for j in range(len(positions)):
                species = atom_species[j]  # 원자 종류는 ID로 설정
                pos = positions[j]  # 포지션
                force = forces[j] # 힘

                # extxyz 형식으로 작성
                #f.write(f"{species} {pos[0]} {pos[1]} {pos[2]} {force[0]} {force[1]} {force[2]}\n")
                #f.write(f"{species}\t{pos[0]}\t{pos[1]}\t{pos[2]}\t{force[0]}\t{force[1]}\t{force[2]}\n")
                f.write(f"{species:<3}\t{pos[0]:>15.8f}\t{pos[1]:>15.8f}\t{pos[2]:>15.8f}\t{force[0]:>15.8f}\t{force[1]:>15.8f}\t{force[2]:>15.8f}\n")

print(f"extxyz data saved to {output_file}")

                #force_str = " ".join(map(str, forces[j]))  # 힘을 문자열로 변환
                #f.write(f"{species} {pos[0]} {pos[1]} {pos[2]} {force_str}\n")
