<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\BulkStoreUsersRequest;
use App\Models\User;
use Carbon\Carbon;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class UserController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $perPage = min(max((int) $request->query('per_page', 20), 1), 200);

        $users = User::paginate($perPage);

        return response()->json($users);
    }

    public function emails(Request $request): JsonResponse
    {
        $perPage = min(max((int) $request->query('per_page', 20), 1), 200);

        $users = User::select('id', 'email')->paginate($perPage);

        return response()->json($users);
    }

    public function overTwenty(Request $request): JsonResponse
    {
        $perPage = min(max((int) $request->query('per_page', 20), 1), 200);

        $cutoff = Carbon::now()->subYears(20)->startOfDay();

        $users = User::whereDate('birth_date', '<=', $cutoff)
            ->paginate($perPage);

        return response()->json($users);
    }

    public function bulkStore(BulkStoreUsersRequest $request): JsonResponse
    {
        $created = [];

        foreach ($request->validated()['users'] as $userData) {
            $created[] = User::create([
                'name' => $userData['name'],
                'email' => $userData['email'],
                'birth_date' => $userData['birth_date'],
                'password' => Hash::make($userData['password'] ?? 'password'),
            ]);
        }

        return response()->json([
            'message' => 'Se crearon 3 usuarios correctamente.',
            'users' => $created,
        ], 201);
    }
}